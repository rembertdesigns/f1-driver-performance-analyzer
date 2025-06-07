# 🏎️ F1 Driver Performance Analyzer

An interactive, multi-view dashboard built with Python and Streamlit to analyze and compare Formula 1 driver performance from historical race data.

This application provides a suite of tools for exploring lap times, comparing drivers head-to-head, analyzing teammate performance, breaking down stints, and even uses a machine learning model to generate a performance score for each driver.

---

## ✨ Key Features

### Modern Tabbed Dashboard
A clean, intuitive user interface built with `st.tabs` that organizes different analyses into logical sections for easy navigation.

### Interactive Data Visualization
All charts are created with Plotly for a rich, interactive experience, including tooltips, zoom, and pan capabilities.

### Comprehensive Analysis Views
- **Summary Insights**: High-level metrics at a glance, including fastest average lap, most consistent stint, and biggest performance drop-off.
- **Driver vs. Driver**: A head-to-head lap time comparison between any two drivers in the race.
- **Teammate Comparison**: The ultimate F1 benchmark, comparing two drivers in the same machinery.
- **Stint & Tyre Performance**: Analyze pace degradation and performance across different tire stints and compounds.

### AI-Powered Scoring
Integrates a pre-trained Scikit-learn model (`driver_score_model.pkl`) to generate a performance score for each driver based on key race metrics, with results displayed in a styled table.

### Robust Data Handling
The app gracefully handles different data formats and includes checks for missing or invalid data to ensure a smooth user experience.

### Dynamic Filtering
Users can easily select the **year** and **race** they want to analyze from the available data.

---

## 🛠️ Technologies Used

- **Core**: Python 3.10+
- **User Interface & Visualization**: Streamlit, Plotly, Pandas
- **Machine Learning**: Scikit-learn, Joblib
- **Data Handling**: NumPy, Pandas

---

## 🧱 Project Structure

```bash
f1-driver-performance-analyzer/
│
├── data/
│ └── sessions/
│ └── e.g., 2024_Bahrain_Grand_Prix_RACE.csv
│
├── models/
│ └── driver_score_model.pkl
│
├── streamlit_app/
│ └── app.py # The main Streamlit application script
│
├── notebooks/
│ └── EDA.ipynb # Exploratory Data Analysis notebook
│
├── src/
│ └── data_loader.py # Example helper script
│
├── train_model.py # Script to train the driver score model
├── requirements.txt # Python package dependencies
└── README.md
```
---

## 🚀 Run It Locally

```bash

git clone https://github.com/rembertdesigns/f1-driver-performance-analyzer.git
cd f1-driver-performance-analyzer

# (Optional) Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch app
streamlit run streamlit_app/app.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or newer
- `pip` for package installation

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rembertdesigns/f1-driver-performance-analyzer.git
cd f1-driver-performance-analyzer
```
2. **Create and activate a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows:
venv\Scripts\activate
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
---

## 🚀 Running the Application

> 📁 **Important**: Ensure you have the necessary `.csv` race data in `data/sessions/` and the trained model `driver_score_model.pkl` in `models/`.

From the project root, run:

```bash
streamlit run streamlit_app/app.py
```
Then open the URL in your browser (typically http://localhost:8501).

---

## 🛣️ Future Enhancements

- **Integrate Telemetry Data**
Use the `fastf1` library to pull and visualize detailed telemetry (speed, throttle, brake) for head-to-head lap comparisons.
- **Race Start Analysis**
Show positions gained or lost on the opening lap.
- **Qualifying Data Integration**
Load and compare qualifying results, including season teammate head-to-head records.
- **Driver & Team Season Summaries**
Aggregate performance data across an entire season.
- **Saving/Loading App State**
Allow saving current selections to a shareable URL.

---

## 📄 License
This project is licensed under the MIT License.
