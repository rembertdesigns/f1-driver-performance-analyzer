import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Set Streamlit page config
st.set_page_config(
    page_title="F1 Driver Performance Analyzer",
    layout="wide",
    page_icon="🏎️"
)

st.markdown("<h1 style='font-size: 40px;'>🏎️ F1 Race Fastest & Most Consistent Driver</h1>", unsafe_allow_html=True)

# Sidebar layout
col1, col2, col3 = st.columns([2, 2, 4])

# View selector
with col1:
    st.markdown("### 🧭 Select View")
    view = st.radio("", [
        "Fastest & Most Consistent Driver",
        "Driver vs Driver",
        "Teammate Comparison",
        "Career Overview"
    ])

# Year selector
session_path = "data/sessions"
available_files = [f for f in os.listdir(session_path) if f.endswith(".csv")]
available_years = sorted(list(set([f.split("_")[0] for f in available_files])))

with col2:
    st.markdown("### Select Year")
    selected_year = st.selectbox("", available_years)

# Race selector
races = sorted([f for f in available_files if f.startswith(selected_year)])
readable_races = {r: r.replace("_", " ").replace(" Grand Prix RACE.csv", " Grand Prix") for r in races}

with col3:
    st.markdown("### Select Race")
    selected_race_file = st.selectbox("", races, format_func=lambda x: readable_races[x])

# Load selected race data
race_path = os.path.join(session_path, selected_race_file)
df = pd.read_csv(race_path)
df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"], errors='coerce').dt.total_seconds()

if view == "Fastest & Most Consistent Driver":
    st.markdown(f"## {readable_races[selected_race_file]} - Driver Analysis")

    df_valid = df.dropna(subset=["LapTimeSeconds"])
    fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
    std_dev = df_valid.groupby("Driver")["LapTimeSeconds"].std()

    fastest_driver = fastest_laps.idxmin()
    fastest_time = round(fastest_laps.min(), 3)
    consistent_driver = std_dev.idxmin()
    consistent_value = round(std_dev.min(), 3)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ⚡ Fastest Driver")
        st.subheader(f"{fastest_driver}")
        st.success(f"{fastest_time}s")

    with col2:
        st.markdown("#### 💕 Most Consistent")
        st.subheader(f"{consistent_driver}")
        st.success(f"±{consistent_value}s")

    st.markdown("### 🗂️ Raw Lap Data")
    st.dataframe(df, use_container_width=True)

elif view == "Driver vs Driver":
    st.markdown(f"## 🏁 {readable_races[selected_race_file]} - Driver Comparison")

    driver_options = df["Driver"].unique().tolist()
    driver1 = st.selectbox("Select Driver 1", driver_options)
    driver2 = st.selectbox("Select Driver 2", driver_options, index=1 if len(driver_options) > 1 else 0)

    fig, ax = plt.subplots()
    for driver in [driver1, driver2]:
        df_driver = df[df["Driver"] == driver]
        ax.plot(df_driver["LapNumber"], df_driver["LapTimeSeconds"], label=driver)

    ax.set_title(f"Lap Time Comparison: {driver1} vs {driver2}")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.legend()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    st.pyplot(fig)

elif view == "Teammate Comparison":
    st.markdown(f"## 🧑‍🤝‍🧑 Teammate Lap Time Comparison - {readable_races[selected_race_file]}")

    team_options = df["Team"].dropna().unique().tolist()
    selected_team = st.selectbox("Select Team", team_options)

    teammates = df[df["Team"] == selected_team]["Driver"].unique()
    if len(teammates) == 2:
        fig, ax = plt.subplots()
        for driver in teammates:
            df_driver = df[df["Driver"] == driver]
            ax.plot(df_driver["LapNumber"], df_driver["LapTimeSeconds"], label=driver, marker="o")

        ax.set_title(f"Lap Time Comparison: {teammates[0]} vs {teammates[1]}")
        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time (s)")
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        st.pyplot(fig)
    else:
        st.warning("This team does not have exactly two drivers in this session.")

elif view == "Career Overview":
    st.markdown("## 📈 Driver Career Overview (Coming Soon)")
    st.info("This feature is under development and will be live in a future update.")












