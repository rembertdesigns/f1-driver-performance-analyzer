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

## 📈 Roadmap

 - Build lap comparison & teammate tabs
 - Add stint + tire compound analysis
 - Train ML model for driver scoring
 - Add summary insights panel
 - Launch to Streamlit Community Cloud
 - Add seasonal teammate battles
 - Implement driver trend dashboard
 - Add advanced metrics: overtakes, tire degradation rate
 - Optional: upgrade model to deep learning (attention-based)

 ---
 
## 🧠 Sample Insight: AI Driver Scoring

Using features like:

- Stint average length
- Lap time consistency (std dev)
- Tire compound usage
- Pace delta vs teammate
  
We score drivers using a trained regression model. This helps compare performance in a normalized way across different races and teams.

 ---

## 🔍 Keywords for Discoverability

```
F1 analytics, Formula 1, driver comparison, teammate battle, stint analysis, tire strategy, lap time analysis, Streamlit F1, F1 data app, motorsport ML, AI in racing, race telemetry, FastF1, driver scoring model
```
 ---
 
## 🤝 Contributions Welcome

Open to pull requests, issue reports, or feedback. Want to help with tire modeling or ML enhancements? Let’s talk.

## 📬 Connect

- LinkedIn → [Richard Rembert](https://www.linkedin.com/in/rrembert/)
- Twitter → [@RichardDRembert](https://x.com/RichardDRembert)

## 📄 License

MIT License
