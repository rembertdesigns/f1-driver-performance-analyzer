# 🏎️ F1 Driver Performance Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://f1-driver-performance-analyzer.streamlit.app/)

An interactive, multi-view dashboard built with Python and Streamlit to analyze and compare Formula 1 driver performance from historical race data using FastF1 telemetry.

This application provides a comprehensive suite of tools for exploring lap times, comparing drivers head-to-head, analyzing teammate performance, breaking down stints, and even uses a machine learning model to generate performance scores for each driver.

---

## ✨ Key Features

### Modern Tabbed Dashboard
A clean, intuitive user interface built with `st.tabs` that organizes different analyses into logical sections for easy navigation.

### Interactive Data Visualization
All charts are created with Plotly for a rich, interactive experience, including tooltips, zoom, and pan capabilities.

### Comprehensive Analysis Views
- **📊 Summary Insights**: High-level race metrics including fastest average lap, most consistent stint, and biggest performance drop-off
- **⚡ Fastest & Consistent**: Identify the fastest single lap and most consistent driver performances
- **⚔️ Driver vs. Driver**: Head-to-head lap time comparison between any two drivers in the race
- **👥 Teammate Comparison**: The ultimate F1 benchmark - comparing drivers in identical machinery
- **🧪 Stint Performance**: Analyze pace degradation and performance across different tire stints
- **🛞 Tyre Compounds**: Performance analysis by tire compound (Soft, Medium, Hard)
- **🧠 AI Driver Scoring**: ML-powered performance scoring based on key race metrics

### AI-Powered Performance Scoring
Integrates a pre-trained Scikit-learn model (`driver_score_model.pkl`) to generate comprehensive performance scores for each driver based on:
- Pace relative to teammate
- Lap time consistency (standard deviation)
- Average stint length
- Tire compound strategy

### Robust Data Handling
- Graceful handling of different CSV formats and missing data
- Comprehensive error checking and user feedback
- Dynamic filtering by year and race

---

## 🛠️ Technologies Used

- **Core**: Python 3.10+
- **Data Analysis**: FastF1, Pandas, NumPy
- **Visualization**: Streamlit, Plotly Express
- **Machine Learning**: Scikit-learn, Joblib
- **Model Explainability**: SHAP (Shapley Additive Explanations)

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
