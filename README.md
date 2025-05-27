# 🏎️ F1 Driver Performance Analyzer

An interactive Streamlit app that breaks down Formula 1 driver performance using lap-by-lap data, stint strategy, tire compound trends, and AI-powered scoring. Perfect for fans, analysts, and engineers who want data-driven insights at their fingertips.

🔗 **Live App**: [Streamlit Community Cloud](https://f1-driver-performance-analyzer.streamlit.app/)  
📦 **Repo**: https://github.com/rembertdesigns/f1-driver-performance-analyzer

---

## 📊 What It Does

This tool lets users explore any F1 race (2018–2022) and compare drivers on key performance metrics like lap time consistency, stint strategy, tire degradation, and more. It also includes an AI-driven scoring engine to rate drivers based on pace, tire use, and teammate delta.

---

## 🧠 Key Features

- 🧭 **Race Selector** – Choose year & race dynamically (based on CSVs in `data/sessions/`)
- ⚡ **Fastest & Most Consistent Driver** – See who had the fastest lap and most stable pace
- 🆚 **Driver vs Driver** – Head-to-head lap time comparison
- 👥 **Teammate Comparison** – Analyze intra-team performance
- 📈 **Career Overview** – View all races a driver participated in
- 🧪 **Stint Performance Breakdown** – Track pace drop-off across stints
- 🛞 **Tyre Compound Viewer** – Analyze lap times based on compound type
- 🧠 **Summary Insights** – Key race takeaways: fastest avg lap, consistency, pit impact
- 🏁 **Driver Scoring (AI)** – Predict scores using regression model trained on stint & tire data

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Data Source**: Preprocessed FastF1 data in CSV format
- **ML Engine**: Scikit-learn (Linear Regression)
- **Visualization**: Matplotlib
- **Model Storage**: `joblib` + `models/` directory

---

## 📁 File Structure

```bash
.
├── streamlit_app/
│   ├── app.py                # Main Streamlit app
│   ├── train_model.py        # ML training script
│   ├── inspect_model.py      # Helper script to debug features
├── data/
│   └── sessions/             # Race .csv files
├── models/
│   └── driver_score_model.pkl
├── requirements.txt
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
