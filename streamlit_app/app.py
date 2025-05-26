import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# --- Set Page Config ---
st.set_page_config(page_title="F1 Race Analyzer", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🏁 Navigation")
view_mode = st.sidebar.radio("Select View", ["Fastest & Most Consistent Driver", "Driver vs Driver", "Teammate Comparison"])

# --- Year and Race Selector ---
st.sidebar.subheader("Select Race")
data_dir = "data/sessions"
all_files = sorted(f for f in os.listdir(data_dir) if f.endswith(".csv"))
years = sorted(list(set(f.split("_")[0] for f in all_files)))
selected_year = st.sidebar.selectbox("Select Year", years)

races = [f for f in all_files if f.startswith(selected_year)]
race_titles = [f.replace(".csv", "").replace("_", " ") for f in races]
race_map = dict(zip(race_titles, races))
selected_race_title = st.sidebar.selectbox("Select Race", race_titles)
selected_file = race_map[selected_race_title]

# --- Load Data ---
df = pd.read_csv(os.path.join(data_dir, selected_file))
df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"]).dt.total_seconds()
df_valid = df[df["LapTimeSeconds"].notna() & (df["LapTimeSeconds"] > 0)]

# --- Feature 1: Fastest & Most Consistent Driver ---
if view_mode == "Fastest & Most Consistent Driver":
    st.title("🏎️ F1 Race Fastest & Most Consistent Driver")
    st.subheader(f"{selected_race_title}")

    fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
    fastest_driver = fastest_laps.idxmin()
    fastest_time = fastest_laps.min()

    consistency = df_valid.groupby("Driver")["LapTimeSeconds"].std()
    consistent_driver = consistency.idxmin()
    consistent_std = consistency.min()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("⚡ Fastest Driver", fastest_driver, f"{fastest_time:.3f}s")
    with col2:
        st.metric("💕 Most Consistent", consistent_driver, f"±{consistent_std:.3f}s")

    st.markdown("📄 **Raw Lap Data**")
    st.dataframe(df_valid)

# --- Feature 2: Driver vs Driver Comparison ---
elif view_mode == "Driver vs Driver":
    st.title(f"🏁 {selected_race_title} - Driver Comparison")
    drivers = df["Driver"].dropna().unique().tolist()
    col1, col2 = st.columns(2)
    driver1 = col1.selectbox("Select Driver 1", drivers, index=0)
    driver2 = col2.selectbox("Select Driver 2", drivers, index=1)

    fig, ax = plt.subplots()
    for driver in [driver1, driver2]:
        df_driver = df_valid[df_valid["Driver"] == driver]
        ax.plot(df_driver["LapNumber"], df_driver["LapTimeSeconds"], label=driver)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.set_title(f"Lap Time Comparison: {driver1} vs {driver2}")
    ax.legend()
    st.pyplot(fig)

# --- Feature 3: Teammate Comparison ---
elif view_mode == "Teammate Comparison":
    st.title(f"👥 Teammate Lap Time Comparison - {selected_race_title}")
    teams = df["Team"].dropna().unique().tolist()
    selected_team = st.selectbox("Select Team", teams)

    df_team = df_valid[df_valid["Team"] == selected_team]
    team_drivers = df_team["Driver"].unique()

    if len(team_drivers) == 2:
        driver1, driver2 = team_drivers
        fig, ax = plt.subplots()
        for driver in [driver1, driver2]:
            df_driver = df_team[df_team["Driver"] == driver]
            ax.plot(df_driver["LapNumber"], df_driver["LapTimeSeconds"], label=driver, marker='o')
        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time (s)")
        ax.set_title(f"Lap Time Comparison: {driver1} vs {driver2}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("This team doesn't have exactly 2 drivers for this race.")


