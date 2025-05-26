import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

st.set_page_config(layout="wide")

# Set Streamlit theme
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    .stRadio > div {
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# Load available races
def load_race_files():
    race_files = sorted(glob("data/sessions/*.csv"))
    races = {}
    for file in race_files:
        name = os.path.basename(file).replace(".csv", "")
        clean_name = name.replace("_RACE", "").replace("_", " ")
        year = name.split("_")[0]
        if year not in races:
            races[year] = []
        races[year].append((clean_name, file))
    return races

races_by_year = load_race_files()

# Sidebar Navigation
st.sidebar.title("🏁 Navigation")
view = st.sidebar.radio("Select View", [
    "Fastest & Most Consistent Driver",
    "Driver vs Driver",
    "Teammate Comparison",
    "Career Summary"
])

# Sidebar: Select Year and Race
years = sorted(races_by_year.keys())
selected_year = st.sidebar.selectbox("Select Year", years)
selected_race_name, selected_race_path = st.sidebar.selectbox(
    "Select Race", races_by_year[selected_year], format_func=lambda x: x[0]
)

# Load data for selected race
df = pd.read_csv(selected_race_path)
df["LapTimeSeconds"] = pd.to_timedelta(df["LapTime"]).dt.total_seconds()

# Fastest & Most Consistent Driver View
if view == "Fastest & Most Consistent Driver":
    st.title("🏎️ F1 Race Fastest & Most Consistent Driver")
    st.subheader(f"{selected_race_name}")

    if df.empty or df["LapTimeSeconds"].isnull().all():
        st.warning("No valid lap data available for this race.")
    else:
        df_valid = df[df["LapTimeSeconds"].notnull()]
        fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
        fastest_driver = fastest_laps.idxmin()
        fastest_time = fastest_laps.min()

        lap_std = df_valid.groupby("Driver")["LapTimeSeconds"].std()
        most_consistent = lap_std.idxmin()
        consistency_value = lap_std.min()

        col1, col2 = st.columns(2)
        col1.metric("⚡ Fastest Driver", fastest_driver, f"↓ {fastest_time:.3f}s")
        col2.metric("💕 Most Consistent", most_consistent, f"±{consistency_value:.3f}s")

        st.subheader("📄 Raw Lap Data")
        st.dataframe(df, use_container_width=True, hide_index=True)

# Driver vs Driver View
elif view == "Driver vs Driver":
    st.title(f"🏁 {selected_race_name} - Driver Comparison")
    drivers = df["Driver"].unique().tolist()
    d1 = st.selectbox("Select Driver 1", drivers, key="driver1")
    d2 = st.selectbox("Select Driver 2", drivers, key="driver2")

    fig, ax = plt.subplots()
    for d in [d1, d2]:
        d_laps = df[df["Driver"] == d]
        ax.plot(d_laps["LapNumber"], d_laps["LapTimeSeconds"], label=d)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.set_title(f"Lap Time Comparison: {d1} vs {d2}")
    ax.legend()
    st.pyplot(fig)

# Teammate Comparison View
elif view == "Teammate Comparison":
    st.title(f"👥 Teammate Lap Time Comparison - {selected_race_name}")
    teams = df["Team"].dropna().unique().tolist()
    selected_team = st.selectbox("Select Team", teams)
    teammate_data = df[df["Team"] == selected_team]
    teammates = teammate_data["Driver"].unique().tolist()

    fig, ax = plt.subplots()
    for t in teammates:
        t_laps = teammate_data[teammate_data["Driver"] == t]
        ax.plot(t_laps["LapNumber"], t_laps["LapTimeSeconds"], marker='o', label=t)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    ax.set_title(f"Lap Time Comparison: {' vs '.join(teammates)}")
    ax.legend()
    st.pyplot(fig)

# Career Summary View
elif view == "Career Summary":
    st.title("📊 Driver Career Summary")

    # All drivers from all races
    all_driver_data = []
    for year, race_list in races_by_year.items():
        for _, path in race_list:
            try:
                temp_df = pd.read_csv(path)
                temp_df["LapTimeSeconds"] = pd.to_timedelta(temp_df["LapTime"], errors='coerce').dt.total_seconds()
                all_driver_data.append(temp_df)
            except Exception:
                continue

    full_data = pd.concat(all_driver_data, ignore_index=True)
    available_drivers = sorted(full_data["Driver"].dropna().unique())
    selected_driver = st.selectbox("Select Driver", available_drivers)

    driver_df = full_data[full_data["Driver"] == selected_driver]

    total_races = driver_df[["Driver", "LapNumber"]].groupby(driver_df.index // 60).count().shape[0]
    avg_lap_time = driver_df["LapTimeSeconds"].mean()
    min_lap_time = driver_df["LapTimeSeconds"].min()
    max_lap_time = driver_df["LapTimeSeconds"].max()

    st.metric("Total Races Sampled", total_races)
    st.metric("Avg Lap Time", f"{avg_lap_time:.2f} sec")
    st.metric("Fastest Lap", f"{min_lap_time:.2f} sec")
    st.metric("Slowest Lap", f"{max_lap_time:.2f} sec")

    st.subheader("Lap Time Distribution")
    fig, ax = plt.subplots()
    sns.histplot(driver_df["LapTimeSeconds"], bins=30, kde=True, ax=ax)
    ax.set_xlabel("Lap Time (s)")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Lap Time Distribution for {selected_driver}")
    st.pyplot(fig)











