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

# --- Color & Data Dictionaries ---
TEAM_COLORS = {
    "Mercedes": "#00D2BE", "Red Bull Racing": "#0600EF", "Ferrari": "#DC0000",
    "McLaren": "#FF8700", "Aston Martin": "#006F62", "Alpine": "#0090FF",
    "Williams": "#005AFF", "AlphaTauri": "#2B4562", "Kick Sauber": "#00ff00",
    "Haas F1 Team": "#FFFFFF", "RB": "#6692FF"
}

# --- Robust Path Handling ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
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

    df['LapTime'] = df['LapTime'].astype(str)
    df['LapTimeSeconds'] = pd.to_timedelta(df['LapTime'], errors='coerce').dt.total_seconds()
    
    initial_rows = len(df)
    invalid_laptimes_sample = df[df['LapTimeSeconds'].isnull()]['LapTime'].unique()[:5]
    df.dropna(subset=['LapTimeSeconds'], inplace=True)
    valid_rows = len(df)
    
    if valid_rows == 0 and initial_rows > 0:
        error_message = (
            f"File '{os.path.basename(file_path)}' was loaded, but no valid lap times could be parsed. "
            f"Example failed values in 'LapTime' column: {invalid_laptimes_sample}"
        )
        return pd.DataFrame(), error_message

    return df, None

# --- Sidebar for Global Filters ---
st.sidebar.header(" Race Selection")

if not os.path.exists(DATA_DIR):
    st.sidebar.error(f"Data directory not found at the expected location: '{os.path.abspath(DATA_DIR)}'. Please check your project structure.")
    st.stop()

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
    df, error_msg = load_session_data(os.path.join(DATA_DIR, selected_race_file))
except (KeyError, FileNotFoundError):
    st.error("Could not find or load the selected race data. Please check your data directory.")
    st.stop()

if error_msg: st.warning(error_msg); st.stop()
if df.empty: st.warning("The selected data file is empty or could not be loaded correctly."); st.stop()


st.header(f"Analysis for {selected_race_label} - {selected_year}")
st.markdown(f"Displaying analysis for **{df['Driver'].nunique()}** drivers across **{df['LapNumber'].max():.0f}** laps.")
st.divider()

# --- Tabbed Layout for Different Views ---
tab_summary, tab_fastest, tab_compare, tab_teammate, tab_stint, tab_tyre, tab_scoring = st.tabs([
    "📊 Summary Insights", "⚡ Fastest & Consistent", "⚔️ Driver vs Driver",
    "👥 Teammate Comparison", "🧪 Stint Performance", "🛞 Tyre Compounds", "🧠 AI Driver Scoring"
])

# --- TAB 1: Summary Insights ---
with tab_summary:
    st.subheader("Race Summary at a Glance")

    def get_fastest_driver(data):
        if "PitOutTime" not in data.columns or "PitInTime" not in data.columns: return "N/A", 0
        no_pit = data[(data["PitOutTime"].isnull()) & (data["PitInTime"].isnull())]
        if no_pit.empty: return "N/A", 0
        fastest_avg = no_pit.groupby("Driver")["LapTimeSeconds"].mean()
        return (fastest_avg.idxmin(), round(fastest_avg.min(), 3)) if not fastest_avg.empty else ("N/A", 0)

    def get_most_consistent_stint(data):
        if data.empty or "Stint" not in data.columns: return ("N/A", "N/A"), 0
        consistency = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].std().dropna()
        return (consistency.idxmin(), round(consistency.min(), 3)) if not consistency.empty else (("N/A", "N/A"), 0)

    def get_biggest_dropoff(data):
        if data.empty or "Stint" not in data.columns: return "N/A", 0
        stint_avg = data.groupby(["Driver", "Stint"])['LapTimeSeconds'].mean().unstack()
        if stint_avg.shape[1] < 2: return "N/A", 0
        dropoff = (stint_avg.diff(axis=1)).max(axis=1).dropna()
        return (dropoff.idxmax(), round(dropoff.max(), 3)) if not dropoff.empty else ("N/A", 0)
    
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
        return max(impacts, key=lambda x: x[1]) if impacts else (None, None)

    col1, col2 = st.columns(2)
    with col1:
        fastest_driver, fastest_avg = get_fastest_driver(df)
        st.metric("🏁 Fastest Avg Lap (no pits)", fastest_driver, f"{fastest_avg}s")
    with col2:
        (cons_driver, stint), consist_std = get_most_consistent_stint(df)
        st.metric("🔁 Most Consistent Stint", f"{cons_driver} - Stint {int(stint) if pd.notna(stint) else 'N/A'}", f"±{consist_std}s")
    
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
        consistency = df_valid.groupby("Driver")["LapTimeSeconds"].std().dropna()

        col1, col2 = st.columns(2)
        if not fastest_laps.empty:
            col1.metric("⚡ Fastest Single Lap", fastest_laps.idxmin(), f"{fastest_laps.min():.3f}s")
        if not consistency.empty:
            col2.metric("⚙️ Most Consistent Driver (Lap Time Std Dev)", consistency.idxmin(), f"±{consistency.min():.3f}s")
    else:
        st.warning("Not enough valid data to determine fastest or most consistent driver.")

    st.subheader("📄 Raw Lap Data")
    st.dataframe(df, use_container_width=True, hide_index=True)


# --- TAB 3: Driver vs Driver ---
with tab_compare:
    st.subheader("Head-to-Head Lap Time Comparison")
    drivers_with_teams = df[['Driver', 'Team']].drop_duplicates().sort_values(by="Driver")
    
    if len(drivers_with_teams) >= 2:
        st.markdown("##### Select two drivers to compare:")
        
        if 'd1_select' not in st.session_state: st.session_state.d1_select = drivers_with_teams['Driver'].iloc[0]
        if 'd2_select' not in st.session_state: st.session_state.d2_select = drivers_with_teams['Driver'].iloc[1]

        cols = st.columns(4)
        for i, row in enumerate(drivers_with_teams.itertuples()):
            with cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"**{row.Driver}**"); st.caption(row.Team)
                    if st.button("Select as #1", key=f"d1_{row.Driver}", use_container_width=True):
                        st.session_state.d1_select = row.Driver; st.rerun()
                    if st.button("Select as #2", key=f"d2_{row.Driver}", use_container_width=True):
                        st.session_state.d2_select = row.Driver; st.rerun()

        st.divider()
        c1, c2, c3 = st.columns([1,1,2])
        c1.metric("Driver 1", st.session_state.d1_select or "Not Selected")
        c2.metric("Driver 2", st.session_state.d2_select or "Not Selected")

        if st.session_state.d1_select and st.session_state.d2_select and st.session_state.d1_select != st.session_state.d2_select:
            compare_df = df[df["Driver"].isin([st.session_state.d1_select, st.session_state.d2_select])]
            
            # --- FIX: Defensively get team colors ---
            d1_team_series = compare_df[compare_df['Driver'] == st.session_state.d1_select]['Team']
            d2_team_series = compare_df[compare_df['Driver'] == st.session_state.d2_select]['Team']

            if not d1_team_series.empty and not d2_team_series.empty:
                d1_team = d1_team_series.iloc[0]
                d2_team = d2_team_series.iloc[0]
                driver_color_map = {
                    st.session_state.d1_select: TEAM_COLORS.get(d1_team, "#FFFFFF"),
                    st.session_state.d2_select: TEAM_COLORS.get(d2_team, "#CCCCCC")
                }

                fig = px.line(
                    compare_df, x="LapNumber", y="LapTimeSeconds", color="Driver",
                    title=f"Lap Time Comparison: {st.session_state.d1_select} vs {st.session_state.d2_select}",
                    labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"},
                    markers=True, color_discrete_map=driver_color_map
                )
                fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<extra></extra>')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not find data for one of the selected drivers to generate plot.")
        else:
            st.info("Please select two different drivers using the buttons above.")
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
            team_color = TEAM_COLORS.get(selected_team, "#CCCCCC") 
            fig = px.line(
                teammate_data, x="LapNumber", y="LapTimeSeconds", color="Driver",
                title=f"Teammate Comparison: {selected_team}",
                labels={"LapNumber": "Lap Number", "LapTimeSeconds": "Lap Time (s)"},
                markers=True, color_discrete_sequence=px.colors.qualitative.Plotly
            )
            if len(fig.data) == 2:
                fig.data[0].line.color = team_color; fig.data[0].line.dash = 'solid'
                fig.data[1].line.color = team_color; fig.data[1].line.dash = 'dot'
            fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<br>Compound: %{customdata[0]}<extra></extra>',
                              customdata=teammate_data[['Compound']])
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("🔍 Analysis & Interpretation"):
                st.markdown("""This chart directly compares teammates in the same machinery, providing one of the purest measures of driver performance.
                - **Crossover Points:** Laps where one driver becomes faster than the other can indicate who managed their tires better or who adapted to changing conditions.
                - **Consistent Gaps:** A consistent gap in favor of one driver can signify a clear pace advantage during this race.""")
        elif len(teammates) == 1: st.warning(f"Only one driver ({teammates[0]}) found for {selected_team} in this race's data.")
        else: st.warning(f"No driver data found for {selected_team}.")


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
            markers=True, category_orders={"Stint": sorted(stint_data["Stint"].unique())}
        )
        fig.update_traces(hovertemplate='<b>Lap %{x}</b><br>Time: %{y:.3f}s<br>Tire: %{customdata[0]}<extra></extra>',
                          customdata=stint_data[['Compound']])
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("🔍 Analysis & Interpretation"):
            st.markdown("""This chart shows the driver's pace across different stints.
            * **Pace Drop-off:** A rising trend in lap times within a single stint indicates high tire degradation (the "performance cliff").
            * **Stint-to-Stint Pace:** Comparing the starting pace of a new stint to the previous one shows the benefit of fresh tires.
            * **Out-Lap vs. In-Lap:** The first lap of a stint (out-lap) is often slower. The last lap before pitting (in-lap) is often faster if the driver is pushing hard.""")

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
    st.info("This score is generated by a pre-trained model that evaluates performance based on several key metrics from the race.")
    MODEL_PATH = os.path.join(MODELS_DIR, "driver_score_model.pkl")

    try:
        model = joblib.load(MODEL_PATH)
        df_valid = df.dropna(subset=["LapTimeSeconds", "Team", "Compound"])
        if df_valid.empty:
            st.warning("No valid lap data available for scoring.")
        else:
            df_valid["TeamAvg"] = df_valid.groupby("Team")["LapTimeSeconds"].transform("mean")
            df_valid["pace_vs_teammate"] = df_valid["TeamAvg"] - df_valid["LapTimeSeconds"]
            df_valid["lap_time_std_dev"] = df_valid.groupby("Driver")["LapTimeSeconds"].transform("std")
            df_valid["avg_stint_length"] = df_valid.groupby(["Driver", "Stint"])["Stint"].transform("count")
            df_valid["compound_type"] = df_valid["Compound"].map({"SOFT": 0, "MEDIUM": 1, "HARD": 2}).fillna(3)
            driver_features = df_valid.groupby("Driver")[["pace_vs_teammate", "lap_time_std_dev", "avg_stint_length", "compound_type"]].mean().dropna()
            
            if driver_features.empty:
                st.warning("Not enough data to generate features for any driver.")
            else:
                scores = model.predict(driver_features)
                driver_features["PredictedScore"] = scores
                st.markdown("#### 🧠 **Predicted Driver Scores** (Higher is Better)")
                st.dataframe(
                    driver_features.sort_values("PredictedScore", ascending=False).style.format("{:.4f}")
                    .background_gradient(subset=["PredictedScore"], cmap="Greens")
                    .set_properties(**{"text-align": "center", "border": "1px solid #444"}),
                    use_container_width=True, hide_index=False
                )
    except FileNotFoundError:
        st.error(f"Model file not found. Please ensure '{os.path.abspath(MODEL_PATH)}' exists.")
    except Exception as e:
        st.error(f"An error occurred during scoring: {e}")