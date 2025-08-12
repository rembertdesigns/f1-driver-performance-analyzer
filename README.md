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

# 🧱 Project Structure

```bash
f1-driver-performance-analyzer/
│
├── data/
│   └── sessions/              # Race CSV files (auto-generated)
│       └── YYYY_RaceName_RACE.csv
│
├── models/
│   └── driver_score_model.pkl # Pre-trained ML model
│
├── streamlit_app/
│   ├── app.py                 # Main Streamlit application
│   └── inspect_model.py       # Model inspection utility
│
├── notebooks/
│   └── EDA.ipynb             # Exploratory Data Analysis
│
├── src/
│   ├── __init__.py
│   └── data_loader.py        # FastF1 data collection script
│
├── train_model.py            # ML model training script
├── requirements.txt          # Python dependencies
└── README.md
```
---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or newer
- `pip` for package installation

### Installation

1. **Clone the repository:**
```
git clone https://github.com/rembertdesigns/f1-driver-performance-analyzer.git
cd f1-driver-performance-analyzer
```
2. **Create and activate a virtual environment (recommended):**
```
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```
3. **Install dependencies:**
```
pip install -r requirements.txt
```
### Data Collection

4. **Collect F1 race data using FastF1:**
```
python src/data_loader.py
```
This will download race data from 2018-2024 and save CSV files to `data/sessions/`.

### Model Training

5. **Train the AI scoring model:**
```
python train_model.py
```
This creates `driver_score_model.pkl` in the `models/ directory`.

### Running the Application

6. **Launch the Streamlit app:**
```
streamlit run streamlit_app/app.py
```
Then open your browser to the URL shown (typically http://localhost:8501).
