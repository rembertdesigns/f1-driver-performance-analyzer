# === app.py ===
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib

# Page setup
st.set_page_config(layout="wide")
st.title("🏎️ F1 Driver Performance Analyzer")

# Sidebar view selector
view = st.radio("🧭 Select View", [
    "Fastest & Most Consistent Driver",
    "Driver vs Driver",
    "Teammate Comparison",
    "Stint Performance Breakdown",
    "Tyre Compound Performance Viewer",
    "Summary Insights",
    "Driver Scoring"
])

# Select Year and Race
years = sorted({f.split("_")[0] for f in os.listdir("data/sessions") if f.endswith(".csv")})
selected_year = st.selectbox("Select Year", years)
race_files = [f for f in os.listdir("data/sessions") if f.startswith(selected_year)]
race_labels = [f.replace(".csv", "").replace("_RACE", "").replace("_", " ") for f in race_files]
race_file_map = dict(zip(race_labels, race_files))
selected_race_label = st.selectbox("Select Race", race_labels)
selected_race_file = race_file_map[selected_race_label]

# Load data
df = pd.read_csv(f"data/sessions/{selected_race_file}")
if df["LapTime"].dtype != "float64":
    df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"], errors="coerce").dt.total_seconds()
else:
    df["LapTimeSeconds"] = df["LapTime"]

# ---------- DRIVER SCORING ----------
if view == "Driver Scoring":
    st.subheader(f"🏁 AI Driver Scoring - {selected_race_label}")
    import joblib

    model = joblib.load("models/driver_score_model.pkl")

    df_valid = df.dropna(subset=["LapTimeSeconds", "Team", "Compound"])
    if df_valid.empty:
        st.warning("No valid lap data available.")
    else:
        # ➕ Compute features
        df_valid["TeamAvg"] = df_valid.groupby("Team")["LapTimeSeconds"].transform("mean")
        df_valid["pace_vs_teammate"] = df_valid["TeamAvg"] - df_valid["LapTimeSeconds"]
        df_valid["lap_time_std_dev"] = df_valid.groupby("Driver")["LapTimeSeconds"].transform("std")
        df_valid["avg_stint_length"] = df_valid.groupby("Driver")["Stint"].transform("count")
        df_valid["compound_type"] = df_valid["Compound"].map({"SOFT": 0, "MEDIUM": 1, "HARD": 2}).fillna(3)

        # ➕ Aggregate to driver-level
        driver_features = df_valid.groupby("Driver")[[
            "pace_vs_teammate",
            "lap_time_std_dev",
            "avg_stint_length",
            "compound_type"
        ]].mean()

        driver_features = driver_features.dropna()

        # ✅ Predict
        scores = model.predict(driver_features)
        driver_features["Score"] = scores

        # 📊 Show styled DataFrame
        styled_df = (
            driver_features
            .sort_values("Score", ascending=False)
            .style
            .format("{:.4f}")
            .background_gradient(subset=["Score"], cmap="Greens")
            .set_properties(**{
                "text-align": "center",
                "border": "1px solid #444",
                "font-family": "monospace",
            })
        )

        st.markdown("#### 🧠 **Predicted Driver Scores** (Higher is Better)")
        st.dataframe(styled_df, use_container_width=True, hide_index=False)

# ---------- Summary Insights Feature ----------
def get_fastest_driver(data):
    no_pit = data[data["PitOutTime"].isnull() & data["PitInTime"].isnull()]
    return no_pit.groupby("Driver")["LapTimeSeconds"].mean().idxmin(), round(no_pit.groupby("Driver")["LapTimeSeconds"].mean().min(), 3)

def get_most_consistent_stint(data):
    consistency = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].std()
    return consistency.idxmin(), round(consistency.min(), 3)

def get_biggest_dropoff(data):
    stint_avg = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].mean().unstack()
    dropoff = (stint_avg.diff(axis=1)).max(axis=1)
    return dropoff.idxmax(), round(dropoff.max(), 3)

def get_pit_impact(data):
    if "PitInTime" not in data.columns:
        return None, None
    pit_laps = data[data['PitInTime'].notnull()]
    impacts = []
    for _, row in pit_laps.iterrows():
        driver = row['Driver']
        lap = int(row['LapNumber'])
        before = data[(data['Driver'] == driver) & (data['LapNumber'] == lap - 1)]["LapTimeSeconds"]
        after = data[(data['Driver'] == driver) & (data['LapNumber'] == lap + 1)]["LapTimeSeconds"]
        if not before.empty and not after.empty:
            delta = abs(after.values[0] - before.values[0])
            impacts.append((driver, delta))
    if impacts:
        worst = max(impacts, key=lambda x: x[1])
        return worst[0], round(worst[1], 3)
    return None, None

if view == "Summary Insights":
    st.subheader(f"📊 Summary Insights - {selected_race_label}")
    col1, col2 = st.columns(2)
    with col1:
        fastest_driver, fastest_avg = get_fastest_driver(df)
        st.metric("🏁 Fastest Avg Lap (no pits)", fastest_driver, f"{fastest_avg}s")
    with col2:
        (cons_driver, stint), consist_std = get_most_consistent_stint(df)
        st.metric("🔁 Most Consistent Stint", f"{cons_driver} - Stint {stint}", f"±{consist_std}s")
    col3, col4 = st.columns(2)
    with col3:
        fade_driver, drop = get_biggest_dropoff(df)
        st.metric("📉 Biggest Lap Time Fade", fade_driver, f"+{drop}s")
    with col4:
        pit_driver, impact = get_pit_impact(df)
        if pit_driver:
            st.metric("🧪 Pit Strategy Impact", pit_driver, f"Δ{impact}s")
        else:
            st.info("No pit stop data available.")

if view == "Fastest & Most Consistent Driver":
    st.subheader(f"📉 {selected_race_label} - Driver Analysis")
    df_valid = df.dropna(subset=["LapTimeSeconds"])
    fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
    fastest_driver = fastest_laps.idxmin()
    fastest_time = fastest_laps.min()
    consistency = df_valid.groupby("Driver")["LapTimeSeconds"].std()
    most_consistent_driver = consistency.idxmin()
    consistency_time = consistency.min()
    col1, col2 = st.columns(2)
    col1.metric("⚡ Fastest Driver", fastest_driver, f"⬆️ {fastest_time:.3f}s")
    col2.metric("💕 Most Consistent", most_consistent_driver, f"⬆️ ±{consistency_time:.3f}s")
    st.subheader("📄 Raw Lap Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif view == "Driver vs Driver":
    st.subheader(f"🏁 {selected_race_label} - Driver Comparison")
    drivers = df["Driver"].unique()
    driver1 = st.selectbox("Select Driver 1", drivers)
    driver2 = st.selectbox("Select Driver 2", drivers, index=1 if len(drivers) > 1 else 0)
    fig, ax = plt.subplots()
    for driver in [driver1, driver2]:
        driver_data = df[df["Driver"] == driver]
        ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], label=driver)
    ax.set_title(f"Lap Time Comparison: {driver1} vs {driver2}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    st.pyplot(fig)

elif view == "Teammate Comparison":
    st.subheader(f"👥 Teammate Lap Time Comparison - {selected_race_label}")
    teams = df["Team"].dropna().unique()
    selected_team = st.selectbox("Select Team", teams)
    teammates = df[df["Team"] == selected_team]["Driver"].unique()
    fig, ax = plt.subplots()
    for driver in teammates:
        driver_data = df[(df["Driver"] == driver) & (df["Team"] == selected_team)]
        ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], marker="o", label=driver)
    ax.set_title(f"Lap Time Comparison: {' vs '.join(teammates)}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    st.pyplot(fig)

elif view == "Stint Performance Breakdown":
    st.subheader(f"🧪 Stint Performance - {selected_race_label}")
    drivers = df["Driver"].unique()
    selected_driver = st.selectbox("Select Driver", drivers)
    fig, ax = plt.subplots()
    for stint in sorted(df[df["Driver"] == selected_driver]["Stint"].dropna().unique()):
        stint_data = df[(df["Driver"] == selected_driver) & (df["Stint"] == stint)]
        ax.plot(stint_data["LapNumber"], stint_data["LapTimeSeconds"], label=f"Stint {int(stint)}")
    ax.set_title(f"Lap Time by Stint for {selected_driver}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    st.pyplot(fig)

elif view == "Tyre Compound Performance Viewer":
    st.subheader(f"🛞 Tyre Compound Performance - {selected_race_label}")
    
    compound_options = df["Compound"].dropna().unique().tolist()
    selected_compound = st.selectbox("Select Compound", compound_options)
    
    filtered_df = df[df["Compound"] == selected_compound]
    drivers = filtered_df["Driver"].dropna().unique()
    
    fig, ax = plt.subplots()
    for driver in drivers:
        driver_data = filtered_df[filtered_df["Driver"] == driver]
        ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], label=driver)
    
    ax.set_title(f"Lap Times on {selected_compound} Compound")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    
    # ✅ Cleaner, smaller legend outside the chart
    ax.legend(fontsize="x-small", loc="center left", bbox_to_anchor=(1, 0.5))
    
    st.pyplot(fig)















