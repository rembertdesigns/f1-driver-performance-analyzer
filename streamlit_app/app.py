import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Set up the page layout
st.set_page_config(layout="wide", page_title="F1 Driver Analyzer")

# App title
st.sidebar.title("🏁 Navigation")
view = st.sidebar.radio("Select View", [
    "Fastest & Most Consistent Driver",
    "Driver vs Driver",
    "Teammate Comparison",
    "Career Summary"
])

# Load races by year
data_path = "data/sessions"
all_files = sorted([f for f in os.listdir(data_path) if f.endswith(".csv")])

# Extract unique years
available_years = sorted(set([f.split("_")[0] for f in all_files]))
selected_year = st.sidebar.selectbox("Select Year", available_years)
races = [f for f in all_files if f.startswith(selected_year)]

# Clean display names
race_display_names = [
    race_file.replace(".csv", "").replace("_RACE", "").replace("_", " ") for race_file in races
]
race_file_map = dict(zip(race_display_names, races))
selected_display = st.sidebar.selectbox("Select Race", race_display_names)
selected_race_file = race_file_map[selected_display]

# Load the race data
file_path = os.path.join(data_path, selected_race_file)
df = pd.read_csv(file_path)

# Preprocessing
if "LapTime" in df.columns:
    df = df[df["LapTime"].notnull()]
    df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"]).dt.total_seconds()

# View: Fastest & Most Consistent Driver
if view == "Fastest & Most Consistent Driver":
    st.title("🏎️ F1 Race Fastest & Most Consistent Driver")
    st.subheader(selected_display)

    if df.empty or df["LapTimeSeconds"].isnull().all():
        st.warning("No valid lap time data available for this race.")
    else:
        fastest_laps = df.groupby("Driver")["LapTimeSeconds"].min()
        fastest_driver = fastest_laps.idxmin()
        fastest_time = fastest_laps.min()

        std_dev = df.groupby("Driver")["LapTimeSeconds"].std()
        consistent_driver = std_dev.idxmin()
        consistency_value = std_dev.min()

        col1, col2 = st.columns(2)
        col1.metric("⚡ Fastest Driver", fastest_driver, f"↓ {fastest_time:.3f}s")
        col2.metric("💕 Most Consistent", consistent_driver, f"±{consistency_value:.3f}s")

        st.subheader("📄 Raw Lap Data")
        st.dataframe(df)

# View: Driver vs Driver Comparison
elif view == "Driver vs Driver":
    st.title(f"🏁 {selected_display} - Driver Comparison")
    drivers = df["Driver"].unique()
    d1 = st.selectbox("Select Driver 1", drivers, key="d1")
    d2 = st.selectbox("Select Driver 2", drivers, key="d2")

    fig, ax = plt.subplots()
    for driver in [d1, d2]:
        lap_data = df[df["Driver"] == driver]
        ax.plot(lap_data["LapNumber"], lap_data["LapTimeSeconds"], label=driver, marker='o')

    ax.set_title(f"Lap Time Comparison: {d1} vs {d2}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    st.pyplot(fig)

# View: Teammate Comparison
elif view == "Teammate Comparison":
    st.title(f"👥 Teammate Lap Time Comparison - {selected_display}")
    if "Team" not in df.columns:
        st.warning("Team data is not available in this file.")
    else:
        teams = df["Team"].dropna().unique()
        selected_team = st.selectbox("Select Team", teams)
        team_data = df[df["Team"] == selected_team]

        teammates = team_data["Driver"].unique()
        if len(teammates) < 2:
            st.warning("Less than two drivers found for this team.")
        else:
            fig, ax = plt.subplots()
            for driver in teammates:
                driver_data = team_data[team_data["Driver"] == driver]
                ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], label=driver, marker='o')
            ax.set_title(f"Lap Time Comparison: {teammates[0]} vs {teammates[1]}")
            ax.set_xlabel("Lap Number")
            ax.set_ylabel("Lap Time (s)")
            ax.legend()
            st.pyplot(fig)

# View: Career Summary
elif view == "Career Summary":
    st.title("🏆 Driver Career Summary")
    driver_options = df["Driver"].unique()
    selected_driver = st.selectbox("Select Driver", driver_options)

    driver_df = df[df["Driver"] == selected_driver]

    st.metric("Total Laps Completed", len(driver_df))
    st.metric("Average Lap Time", f"{driver_df['LapTimeSeconds'].mean():.2f} s")
    st.metric("Best Lap Time", f"{driver_df['LapTimeSeconds'].min():.2f} s")

    st.subheader("Lap Times")
    fig, ax = plt.subplots()
    ax.plot(driver_df["LapNumber"], driver_df["LapTimeSeconds"], marker='o')
    ax.set_title(f"Lap Time Trend: {selected_driver}")
    ax.set_xlabel("Lap")
    ax.set_ylabel("Lap Time (s)")
    st.pyplot(fig)

    st.subheader("Driver Lap Summary")
    st.dataframe(driver_df)





