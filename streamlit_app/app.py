import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Set Streamlit page configuration
st.set_page_config(page_title="F1 Driver Performance Analyzer", layout="wide")

# Directory containing session CSVs
data_dir = Path("data/sessions")

# Extract all available years from filenames
def get_available_years():
    return sorted({fname.name[:4] for fname in data_dir.glob("*.csv")})

# Load CSVs by year
@st.cache_data
def load_files_by_year(year):
    files = list(data_dir.glob(f"{year}_*.csv"))
    return sorted(files)

# Load and process race data
@st.cache_data
def load_race_data(filepath):
    df = pd.read_csv(filepath)
    # Clean time-related columns for consistency
    if 'LapTime' in df.columns:
        df['LapTimeSeconds'] = pd.to_timedelta(df['LapTime']).dt.total_seconds()
    return df

# Format race name for display
def format_race_name(filename):
    return filename.stem.replace("_RACE", "").replace("_", " ")

# Styling function for DataFrame display
def style_dataframe(df):
    numeric_cols = df.select_dtypes(include=['number']).columns
    styled = (
        df.style
        .set_properties(**{
            "background-color": "#ffffff",
            "color": "#000000"
        })
        .highlight_max(subset=numeric_cols, axis=0, props='color: #006400; font-weight: bold')
    )
    return styled

# --- Sidebar UI ---
st.sidebar.title("🏁 Navigation")
view_option = st.sidebar.radio("Select View", [
    "Fastest & Most Consistent Driver",
    "Driver vs Driver",
    "Teammate Comparison",
    "Driver Summary"
])

years = get_available_years()
selected_year = st.sidebar.selectbox("Select Year", years)
races = load_files_by_year(selected_year)
formatted_race_names = [format_race_name(f) for f in races]
race_file = st.sidebar.selectbox("Select Race", races, format_func=format_race_name)
df = load_race_data(race_file)

# --- Fastest & Most Consistent ---
if view_option == "Fastest & Most Consistent Driver":
    st.markdown("## 🏎️ F1 Race Fastest & Most Consistent Driver")
    st.subheader(f"{format_race_name(race_file)}")

    df_valid = df[df['LapTimeSeconds'].notna()]
    fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
    lap_std = df_valid.groupby("Driver")["LapTimeSeconds"].std()

    fastest_driver = fastest_laps.idxmin()
    fastest_time = fastest_laps.min()

    consistent_driver = lap_std.idxmin()
    consistency = lap_std.min()

    col1, col2 = st.columns(2)
    col1.metric("⚡ Fastest Driver", fastest_driver, f"↓ {fastest_time:.3f}s")
    col2.metric("💕 Most Consistent", consistent_driver, f"±{consistency:.3f}s")

    st.markdown("### 📄 Raw Lap Data")
    st.dataframe(style_dataframe(df), use_container_width=True, hide_index=True)

# --- Driver vs Driver ---
elif view_option == "Driver vs Driver":
    st.markdown(f"## 🏁 {format_race_name(race_file)} - Driver Comparison")
    drivers = df["Driver"].dropna().unique()
    driver1 = st.selectbox("Select Driver 1", drivers, index=0)
    driver2 = st.selectbox("Select Driver 2", drivers, index=1)

    fig, ax = plt.subplots()
    for d in [driver1, driver2]:
        driver_data = df[df["Driver"] == d]
        ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], label=d)

    ax.set_title(f"Lap Time Comparison: {driver1} vs {driver2}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    st.pyplot(fig)

# --- Teammate Comparison ---
elif view_option == "Teammate Comparison":
    st.markdown(f"## 👥 Teammate Lap Time Comparison - {format_race_name(race_file)}")
    teams = df["Team"].dropna().unique()
    selected_team = st.selectbox("Select Team", teams)

    team_data = df[df["Team"] == selected_team]
    teammates = team_data["Driver"].unique()

    if len(teammates) == 2:
        fig, ax = plt.subplots()
        for t in teammates:
            laps = team_data[team_data["Driver"] == t]
            ax.plot(laps["LapNumber"], laps["LapTimeSeconds"], label=t, marker='o')

        ax.set_title(f"Lap Time Comparison: {teammates[0]} vs {teammates[1]}")
        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time (s)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Selected team does not have exactly 2 drivers in this race.")

# --- Driver Summary ---
elif view_option == "Driver Summary":
    st.markdown(f"## 🧑‍✈️ Driver Summary - {format_race_name(race_file)}")
    drivers = df["Driver"].dropna().unique()
    selected_driver = st.selectbox("Select Driver", drivers)

    driver_data = df[df["Driver"] == selected_driver]

    st.markdown("### 🔍 Lap Time Chart")
    fig, ax = plt.subplots()
    ax.plot(driver_data["LapNumber"], driver_data["LapTimeSeconds"], marker='o')
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.set_title(f"Lap Times for {selected_driver}")
    st.pyplot(fig)

    st.markdown("### 🧾 Full Lap Data")
    st.dataframe(style_dataframe(driver_data), use_container_width=True, hide_index=True)










