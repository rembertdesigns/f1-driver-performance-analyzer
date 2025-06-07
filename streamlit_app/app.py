## === app.py (Enhanced with Tabs, Plotly, and Corrected Paths) ===
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import plotly.express as px

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="F1 Performance Analyzer")
st.title("🏎️ F1 Driver Performance Analyzer")
st.markdown("An interactive dashboard to analyze and compare F1 driver performance for a selected race.")

# --- Robust Path Handling ---
# Get the absolute path of the directory where this script (app.py) is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory by going up one level from 'streamlit_app/'
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))

# Construct absolute paths to data and models directories
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "sessions")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")


# --- Data Loading (Cached for Performance & ENHANCED ERROR HANDLING) ---
@st.cache_data
def load_session_data(file_path):
    """Loads and preprocesses race data from a given file path with detailed error checking."""
    if not os.path.exists(file_path):
        return pd.DataFrame(), f"Data file not found at: {file_path}"
    
    if os.path.getsize(file_path) == 0:
        return pd.DataFrame(), f"File is empty: {os.path.basename(file_path)}"
        
    df = pd.read_csv(file_path)
    
    if "LapTime" not in df.columns:
        return pd.DataFrame(), f"The file '{os.path.basename(file_path)}' is missing the required 'LapTime' column."

    # --- ENHANCED TIME CONVERSION AND DEBUGGING ---
    # First, try to convert to timedelta, which handles '0 days 00:01:23.456' format
    df['LapTimeSeconds'] = pd.to_timedelta(df['LapTime'], errors='coerce').dt.total_seconds()
    
    # If the first method fails for all rows, try a direct numeric conversion
    if df['LapTimeSeconds'].isnull().all():
        df['LapTimeSeconds'] = pd.to_numeric(df['LapTime'], errors='coerce')

    initial_rows = len(df)
    # Get a sample of invalid 'LapTime' values *before* dropping NaNs, for better error messages
    invalid_laptimes_sample = df[df['LapTimeSeconds'].isnull()]['LapTime'].unique()[:5]

    df.dropna(subset=['LapTimeSeconds'], inplace=True)
    valid_rows = len(df)
    
    if valid_rows == 0 and initial_rows > 0:
        error_message = (
            f"File '{os.path.basename(file_path)}' was loaded, but no valid lap times could be parsed from the 'LapTime' column. "
            f"Please check the data format. Here are some example values that failed: {invalid_laptimes_sample}"
        )
        return pd.DataFrame(), error_message

    return df, None # Return None for error message if successful

# --- Sidebar for Global Filters ---
st.sidebar.header(" Race Selection")

if not os.path.exists(DATA_DIR):
    st.sidebar.error(f"Data directory not found at the expected location: '{os.path.abspath(DATA_DIR)}'. Please check your project structure.")
    st.stop()

# Get years from filenames in the corrected directory
all_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
years = sorted({f.split("_")[0] for f in all_files if f.split("_")[0].isdigit()}, reverse=True)

if not years:
    st.sidebar.error(f"No valid data files found in '{DATA_DIR}'. Files should be named like 'YYYY_RaceName_RACE.csv'.")
    st.stop()

selected_year = st.sidebar.selectbox("Select Year", years)

race_files = sorted([f for f in all_files if f.startswith(selected_year)])
race_labels = [f.replace(".csv", "").replace(f"{selected_year}_", "").replace("_RACE", "").replace("_", " ") for f in race_files]
race_file_map = dict(zip(race_labels, race_files))
selected_race_label = st.sidebar.selectbox("Select Race", race_labels)

# --- Main Application Logic ---
try:
    selected_race_file = race_file_map[selected_race_label]
    # load_session_data now returns a tuple (DataFrame, error_message)
    df, error_msg = load_session_data(os.path.join(DATA_DIR, selected_race_file))
except (KeyError, FileNotFoundError):
    st.error("Could not find or load the selected race data. Please check your data directory.")
    st.stop()

# Display the specific error message if one occurred, then stop execution
if error_msg:
    st.warning(error_msg)
    st.stop()


st.header(f"Analysis for {selected_race_label} - {selected_year}")
st.markdown(f"Displaying analysis for **{df['Driver'].nunique()}** drivers across **{df['LapNumber'].max():.0f}** laps.")
st.divider()

# --- Tabbed Layout for Different Views ---
tab_summary, tab_fastest, tab_compare, tab_teammate, tab_stint, tab_tyre, tab_scoring = st.tabs([
    "📊 Summary Insights",
    "⚡ Fastest & Consistent",
    "⚔️ Driver vs Driver",
    "👥 Teammate Comparison",
    "🧪 Stint Performance",
    "🛞 Tyre Compounds",
    "🧠 AI Driver Scoring"
])

# --- TAB 1: Summary Insights ---
with tab_summary:
    st.subheader("Race Summary at a Glance")

    def get_fastest_driver(data):
        if "PitOutTime" not in data.columns or "PitInTime" not in data.columns: return "N/A", 0
        no_pit = data[(data["PitOutTime"].isnull()) & (data["PitInTime"].isnull())]
        if no_pit.empty: return "N/A", 0
        fastest_avg = no_pit.groupby("Driver")["LapTimeSeconds"].mean()
        if fastest_avg.empty: return "N/A", 0
        return fastest_avg.idxmin(), round(fastest_avg.min(), 3)

    def get_most_consistent_stint(data):
        if data.empty or "Stint" not in data.columns: return ("N/A", "N/A"), 0
        consistency = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].std()
        if consistency.empty or consistency.isnull().all(): return ("N/A", "N/A"), 0
        return consistency.idxmin(), round(consistency.min(), 3)

    def get_biggest_dropoff(data):
        if data.empty or "Stint" not in data.columns: return "N/A", 0
        stint_avg = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].mean().unstack()
        if stint_avg.shape[1] < 2: return "N/A", 0
        dropoff = (stint_avg.diff(axis=1)).max(axis=1)
        if dropoff.empty or dropoff.isnull().all(): return "N/A", 0
        return dropoff.idxmax(), round(dropoff.max(), 3)
    
    def get_pit_impact(data):
        if "PitInTime" not in data.columns or data['PitInTime'].isnull().all(): return None, None
        pit_laps = data[data['PitInTime'].notnull()]
        impacts = []
        for _, row in pit_laps.iterrows():
            driver, lap = row['Driver'], int(row['LapNumber'])
            before = data[(data['Driver'] == driver) & (data['LapNumber'] == lap - 1)]["LapTimeSeconds"]
            after = data[(data['Driver'] == driver) & (data['LapNumber'] == lap + 1)]["LapTimeSeconds"]
            if not before.empty and not after.empty:
                delta = abs(after.values[0] - before.values[0])
                impacts.append((driver, delta))
        if impacts: worst = max(impacts, key=lambda x: x[1]); return worst[0], round(worst[1], 3)
        return None, None

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
        st.metric("📉 Biggest Lap Time Fade", fade_driver, f"+{drop}s between stints")
    with col4:
        pit_driver, impact = get_pit_impact(df)
        if pit_driver: st.metric("⏱️ Largest Pit Strategy Time Delta", pit_driver, f"Δ{impact}s around pit")
        else: st.info("No comparable pit stop data available.")


# --- TAB 2: Fastest & Most Consistent ---
with tab_fastest:
    st.subheader("Top Performers Overall")
    df_valid = df.dropna(subset=["LapTimeSeconds"])
    
    if not df_valid.empty:
        fastest_laps = df_valid.groupby("Driver")["LapTimeSeconds"].min()
        fastest_driver = fastest_laps.idxmin()
        fastest_time = fastest_laps.min()

        consistency = df_valid.groupby("Driver")["LapTimeSeconds"].std()
        most_consistent_driver = consistency.idxmin()
        consistency_time = consistency.min()

        col1, col2 = st.columns(2)
        col1.metric("⚡ Fastest Single Lap", fastest_driver, f"{fastest_time:.3f}s")
        col2.metric("⚙️ Most Consistent Driver (Lap Time Std Dev)", most_consistent_driver, f"±{consistency_time:.3f}s")
    else:
        st.warning("Not enough valid data to determine fastest or most consistent driver.")

    st.subheader("📄 Raw Lap Data")
    st.dataframe(df, use_container_width=True, hide_index=True)


# --- TAB 3: Driver vs Driver ---
with tab_compare:
    st.subheader("Head-to-Head Lap Time Comparison")
    drivers = sorted(df["Driver"].unique())
    
    if len(drivers) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            driver1 = st.selectbox("Select Driver 1", drivers, key="d1_select")
        with col2:
            driver2_options = [d for d in drivers if d != driver1]
            driver2 = st.selectbox("Select Driver 2", driver2_options, key="d2_select")

        if driver1 and driver2:
            compare_df = df[df["Driver"].isin([driver1, driver2])]
            fig = px.line(
                compare_df, x="LapNumber", y="LapTimeSeconds", color="Driver",
                title=f"Lap Time Comparison: {driver1} vs {driver2}",
                labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"},
                markers=True
            )
            fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<extra></extra>')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough drivers in the data to make a comparison.")


# --- TAB 4: Teammate Comparison ---
with tab_teammate:
    st.subheader("Teammate Lap Time Comparison")
    teams = sorted(df["Team"].dropna().unique())
    selected_team = st.selectbox("Select Team", teams, key="teammate_team_select")
    
    if selected_team:
        teammates = df[df["Team"] == selected_team]["Driver"].unique()

        if len(teammates) >= 2:
            teammate_data = df[df["Driver"].isin(teammates)]
            fig = px.line(
                teammate_data, x="LapNumber", y="LapTimeSeconds", color="Driver",
                title=f"Teammate Comparison: {selected_team}",
                labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"},
                markers=True
            )
            fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<br>Compound: %{customdata[0]}<extra></extra>',
                              customdata=teammate_data[['Compound']])
            st.plotly_chart(fig, use_container_width=True)
        elif len(teammates) == 1:
            st.warning(f"Only one driver ({teammates[0]}) found for {selected_team} in this race's data.")
        else:
            st.warning(f"No driver data found for {selected_team}.")


# --- TAB 5: Stint Performance ---
with tab_stint:
    st.subheader("Stint Performance Breakdown")
    drivers = sorted(df["Driver"].unique())
    selected_driver_stint = st.selectbox("Select Driver", drivers, key="stint_driver_select")
    
    if selected_driver_stint:
        stint_data = df[df["Driver"] == selected_driver_stint]
        fig = px.line(
            stint_data, x="LapNumber", y="LapTimeSeconds", color="Stint",
            title=f"Lap Times by Stint for {selected_driver_stint}",
            labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"},
            markers=True,
            category_orders={"Stint": sorted(stint_data["Stint"].unique())}
        )
        fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<br>Tire: %{customdata[0]}<extra></extra>',
                          customdata=stint_data[['Compound']])
        st.plotly_chart(fig, use_container_width=True)


# --- TAB 6: Tyre Compounds ---
with tab_tyre:
    st.subheader("Tyre Compound Performance")
    compound_options = sorted(df["Compound"].dropna().unique())
    if compound_options:
        selected_compound = st.selectbox("Select Compound", compound_options, key="tyre_compound_select")
        
        filtered_df = df[df["Compound"] == selected_compound]
        
        fig = px.line(
            filtered_df, x="LapNumber", y="LapTimeSeconds", color="Driver",
            title=f"Lap Times on {selected_compound} Compound",
            labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No compound data available for this race.")


# --- TAB 7: AI Driver Scoring ---
with tab_scoring:
    st.subheader("AI-Powered Driver Score")
    st.info("This score is generated by a pre-trained model (`driver_score_model.pkl`) that evaluates performance based on several key metrics from the race.")
    
    MODEL_PATH = os.path.join(MODELS_DIR, "driver_score_model.pkl")

    try:
        model = joblib.load(MODEL_PATH)

        df_valid = df.dropna(subset=["LapTimeSeconds", "Team", "Compound"])
        if df_valid.empty:
            st.warning("No valid lap data available for scoring.")
        else:
            # --- Feature Engineering ---
            df_valid["TeamAvg"] = df_valid.groupby("Team")["LapTimeSeconds"].transform("mean")
            df_valid["pace_vs_teammate"] = df_valid["TeamAvg"] - df_valid["LapTimeSeconds"]
            df_valid["lap_time_std_dev"] = df_valid.groupby("Driver")["LapTimeSeconds"].transform("std")
            df_valid["avg_stint_length"] = df_valid.groupby(["Driver", "Stint"])["Stint"].transform("count")
            df_valid["compound_type"] = df_valid["Compound"].map({"SOFT": 0, "MEDIUM": 1, "HARD": 2}).fillna(3)

            driver_features = df_valid.groupby("Driver")[[
                "pace_vs_teammate", "lap_time_std_dev", "avg_stint_length", "compound_type"
            ]].mean()
            driver_features = driver_features.dropna()
            
            if driver_features.empty:
                st.warning("Not enough data to generate features for any driver.")
            else:
                # --- Predict Scores ---
                scores = model.predict(driver_features)
                driver_features["PredictedScore"] = scores

                # --- Display Styled DataFrame ---
                st.markdown("#### 🧠 **Predicted Driver Scores** (Higher is Better)")
                st.dataframe(
                    driver_features.sort_values("PredictedScore", ascending=False)
                    .style.format("{:.4f}")
                    .background_gradient(subset=["PredictedScore"], cmap="Greens")
                    .set_properties(**{"text-align": "center", "border": "1px solid #444"}),
                    use_container_width=True, hide_index=False
                )
    except FileNotFoundError:
        st.error(f"Model file not found. Please ensure '{os.path.abspath(MODEL_PATH)}' exists.")
    except Exception as e:
        st.error(f"An error occurred during scoring: {e}")