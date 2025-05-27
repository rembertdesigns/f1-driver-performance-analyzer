import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Define paths
data_dir = "data/sessions"
model_path = "models/driver_score_model.pkl"

# Collect all race CSVs
all_data = []
for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        path = os.path.join(data_dir, file)
        df = pd.read_csv(path)
        race_name = file.replace(".csv", "").replace("_RACE", "").replace("_", " ")
        df["RaceName"] = race_name
        df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"], errors='coerce').dt.total_seconds()
        all_data.append(df)

df_all = pd.concat(all_data, ignore_index=True)

# Feature Engineering
print("🧠 Engineering features...")
# Calculate pace vs teammate
team_avg = df_all.groupby(["RaceName", "Team"])["LapTimeSeconds"].transform("mean")
df_all["pace_vs_teammate"] = team_avg - df_all["LapTimeSeconds"]

# Consistency: std deviation per stint per driver
consistency_map = df_all.groupby(["RaceName", "Driver", "Stint"])["LapTimeSeconds"].transform("std")
df_all["lap_time_std_dev"] = consistency_map

# Avg stint length
stint_lengths = df_all.groupby(["RaceName", "Driver", "Stint"]).size().groupby(level=[0, 1]).mean()
stint_length_map = {(r, d): stint_lengths.loc[(r, d)] for (r, d) in stint_lengths.index}
df_all["avg_stint_length"] = df_all.apply(lambda row: stint_length_map.get((row["RaceName"], row["Driver"]), np.nan), axis=1)

# Encode compound as numeric
compound_map = {name: i for i, name in enumerate(df_all["Compound"].dropna().unique())}
df_all["compound_type"] = df_all["Compound"].map(compound_map)

# Drop NA rows
features = ["pace_vs_teammate", "lap_time_std_dev", "avg_stint_length", "compound_type"]
df_model = df_all.dropna(subset=features)

# Group by driver per race to aggregate
df_features = df_model.groupby(["RaceName", "Driver"])[features].mean().reset_index()

# Target: build synthetic score = weighted average (for now)
df_features["driver_score"] = (
    df_features["pace_vs_teammate"] * 0.5 -
    df_features["lap_time_std_dev"] * 0.3 +
    df_features["avg_stint_length"] * 0.1 -
    df_features["compound_type"] * 0.1
)

# Train/Test Split
X = df_features[features]
y = df_features["driver_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"✅ Model R^2 score: {r2_score(y_test, y_pred):.3f}")

# Save model
joblib.dump(model, model_path)
print(f"💾 Model saved to {model_path}")