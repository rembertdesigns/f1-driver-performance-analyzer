# 🏎️ F1 Driver Performance Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://f1-driver-performance-analyzer.streamlit.app/)

<img width="1776" height="817" alt="Screenshot 2025-08-12 at 10 11 15 AM" src="https://github.com/user-attachments/assets/c9977c19-8d7a-485c-a9d4-1a5c7c9c160d" />


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
<img width="874" height="708" alt="Screenshot 2025-08-12 at 11 00 22 AM" src="https://github.com/user-attachments/assets/a634a0a4-945f-48c9-bcf4-59a61fe95c7a" />

- **⚔️ Driver vs. Driver**: Head-to-head lap time comparison between any two drivers in the race
<img width="1391" height="828" alt="Screenshot 2025-08-12 at 11 02 13 AM" src="https://github.com/user-attachments/assets/7fce2ce7-85c1-4c66-9326-e867394f2fff" />

- **👥 Teammate Comparison**: The ultimate F1 benchmark - comparing drivers in identical machinery
<img width="1398" height="808" alt="Screenshot 2025-08-12 at 11 04 03 AM" src="https://github.com/user-attachments/assets/31986c50-61a2-4613-bb2e-043e8eda0d3c" />

- **🧪 Stint Performance**: Analyze pace degradation and performance across different tire stints
<img width="1390" height="830" alt="Screenshot 2025-08-12 at 11 08 32 AM" src="https://github.com/user-attachments/assets/583dec88-b04f-4b40-a0f6-ea102319131c" />

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

---

## 📊 How It Works

### Data Pipeline
1. **FastF1 Integration**: Automatically downloads telemetry data from Formula 1 races
2. **Feature Engineering**: Calculates key performance metrics like pace vs. teammate and consistency
3. **ML Scoring**: Uses linear regression to score driver performance holistically
4. **Interactive Visualization**: Presents insights through dynamic Plotly charts

### Key Metrics Explained
- **Pace vs. Teammate**: How much faster/slower compared to team average
- **Consistency**: Standard deviation of lap times (lower = more consistent)
- **Stint Analysis**: Performance degradation over tire life
- **Compound Strategy**: Performance differences across tire compounds

---

## 🔍 Model Explainability

The project includes SHAP (SHapley Additive exPlanations) integration to understand:
- Which features most influence driver scores
- How individual predictions are made
- Global feature importance across all drivers

See `notebooks/EDA.ipynb` for detailed model analysis and feature importance visualizations.

---

## 🛣️ Future Enhancements

- **Real-time Data Integration**: Live race analysis during GP weekends
- **Advanced Telemetry**: Speed, throttle, and brake analysis using FastF1's full capabilities
- **Weather Impact Analysis**: Correlation between weather conditions and performance
- **Qualifying Integration**: Compare race pace to qualifying performance
- **Season-long Analytics**: Championship standings and consistency over full seasons
- **Predictive Modeling**: Predict race outcomes based on practice/qualifying data

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastF1**: For providing excellent F1 telemetry data access
- **Formula 1**: For the amazing sport and data availability
- **Streamlit**: For the fantastic web app framework
- **Plotly**: For interactive visualization capabilities

---

## ⚠️ Important Notes

- Race data is sourced from FastF1 and covers seasons from 2018-2024
- Initial data download may take some time due to FastF1 caching
- The ML model is trained on historical data and scores are relative to the dataset
- Some races may have limited telemetry data depending on FastF1 availability
