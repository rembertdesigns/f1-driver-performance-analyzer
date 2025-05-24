import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="F1 Race Explorer", layout="wide")

# Path to sessions
SESSION_DIR = "data/sessions"

# Helper to extract year and race from filenames
def get_race_info():
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith(".csv")]
    races = []
    for f in files:
        parts = f.replace(".csv", "").split("_")
        year = parts[0]
        name = " ".join(parts[1:-1])
        races.append((year, name, f))
    return races

races = get_race_info()

# Create dropdowns
years = sorted(set([r[0] for r in races]), reverse=True)
selected_year = st.sidebar.selectbox("Select Year", years)

race_names = [r[1] for r in races if r[0] == selected_year]
selected_race = st.sidebar.selectbox("Select Race", race_names)

# Load race file
race_file = [r[2] for r in races if r[0] == selected_year and r[1] == selected_race][0]
df = pd.read_csv(os.path.join(SESSION_DIR, race_file))

st.title(f"🏁 {selected_race} {selected_year} - Driver Comparison")

drivers = df['Driver'].unique()
driver1 = st.selectbox("Select Driver 1", drivers, index=0)
driver2 = st.selectbox("Select Driver 2", drivers, index=1)

# Compare stats
st.subheader("📊 Lap Time Comparison")
lap_data = df[df['Driver'].isin([driver1, driver2])]

if not lap_data.empty:
    st.line_chart(lap_data.pivot(index='LapNumber', columns='Driver', values='LapTime'))
else:
    st.warning("No lap time data available for selected drivers.")





