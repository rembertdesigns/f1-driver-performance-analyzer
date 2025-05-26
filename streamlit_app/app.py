import streamlit as st
import pandas as pd
import os

# Paths
DATA_DIR = "./data/sessions"

# Get available years and races
years = sorted({f.split("_")[0] for f in os.listdir(DATA_DIR) if f.endswith(".csv")})
races_by_year = {
    year: sorted([f for f in os.listdir(DATA_DIR) if f.startswith(year) and f.endswith(".csv")])
    for year in years
}

# --- UI
st.set_page_config(page_title="F1 Race Explorer", layout="wide")
st.title("🏎️ F1 Race Fastest & Most Consistent Driver")

# Dropdowns
selected_year = st.sidebar.selectbox("Select Year", years)
selected_race_file = st.sidebar.selectbox("Select Race", races_by_year[selected_year])

# Load session data
df = pd.read_csv(os.path.join(DATA_DIR, selected_race_file))

# Preprocess and validate
if "Driver" in df.columns and "LapTime" in df.columns:
    try:
        df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"]).dt.total_seconds()
        df_valid = df.dropna(subset=["Driver", "LapTimeSeconds"])

        if df_valid.empty or df_valid["LapTimeSeconds"].isnull().all():
            st.error("❌ No valid lap time data found for this session.")
        else:
            # Fastest lap per driver
            fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
            lap_std = df_valid.groupby("Driver")["LapTimeSeconds"].std()

            if not fastest_laps.empty and not lap_std.empty:
                fastest_driver = fastest_laps.idxmin()
                most_consistent = lap_std.idxmin()

                st.subheader(f"{selected_race_file.replace('_', ' ').replace('.csv','')}")
                col1, col2 = st.columns(2)
                col1.metric("⚡ Fastest Driver", fastest_driver, f"{fastest_laps.min():.3f}s")
                col2.metric("🎯 Most Consistent", most_consistent, f"±{lap_std.min():.3f}s")

                st.write("### 📄 Raw Lap Data")
                st.dataframe(df_valid)
            else:
                st.warning("⚠️ Not enough lap data to calculate metrics.")
    except Exception as e:
        st.error(f"❌ Failed to process lap times: {e}")
else:
    st.warning("⚠️ This session file doesn't contain expected columns like 'Driver' and 'LapTime'.")