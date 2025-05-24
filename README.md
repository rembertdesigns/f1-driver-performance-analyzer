# 🏎️ F1 Driver Performance Analyzer

An AI-powered tool that scores Formula 1 drivers based on telemetry data, overtaking stats, race consistency, and pace relative to their teammates. Built for explainability using SHAP and attention mechanisms to uncover what matters most.

---

## 📊 Project Overview

This project analyzes and benchmarks F1 driver performance using machine learning models trained on real race data. It provides interpretable insights into which variables—such as overtakes, pace, and consistency—most influence a driver’s performance rating.

### Goals:
- 🔍 Quantify driver skill in a data-driven, unbiased way
- 🤖 Use AI to spot patterns across different tracks, weather, and team setups
- 🧠 Provide explainable output (via SHAP values or attention maps)
- 📈 Visualize trends across teammates, seasons, and circuits

---

## 🛠️ Tech Stack

- **Language**: Python
- **Notebook Interface**: Jupyter (via Cursor IDE)
- **Data Retrieval**: FastF1 (F1 telemetry + timing)
- **Visualization**: Matplotlib, Seaborn, SHAP
- **ML Modeling**: Scikit-learn (Linear Regression baseline), SHAP
- **Future Option**: TensorFlow or PyTorch for deep models

---

## 🧠 Core Features

- ✅ Load and cache real telemetry data using FastF1
- 📈 Extract pace delta vs. teammate and lap consistency (std dev)
- 🤖 Train regression model to score drivers numerically
- 🔍 Interpret model predictions using SHAP values
- 💾 Export performance vectors and predictions to CSV
- 📊 Save visuals of lap speed profiles and SHAP plots

---

## 📁 Project Structure

---

## 🧪 Example Visuals

### SHAP Summary: What Influences Driver Score?
<img src="visualizations/shap_summary.png" width="600"/>

### Lap Speed Profile: Hamilton at Bahrain FP1
<img src="visualizations/hamilton_speed.png" width="600"/>

---

## 🚀 Run It Locally

```bash
git clone git@github.com:rembertdesigns/f1-driver-performance-analyzer.git
cd f1-driver-performance-analyzer

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch notebook
jupyter notebook
```

---

## 🚧 Roadmap

- [x] Ingest FastF1 telemetry + lap data  
- [x] Feature engineering (pace delta, lap std dev)  
- [x] Train baseline ML model  
- [x] Integrate SHAP for explainability  
- [x] Save predictions and plots to GitHub  
- [ ] Expand to multiple races and drivers  
- [ ] Add overtake & sector-based features  
- [ ] Build dashboard view (Streamlit or Gradio)  
- [ ] Optional: switch to deep learning + attention layers  

---

## 🤝 Contributions Welcome

Have ideas, data sources, or visual improvements? Open an issue or submit a PR!

---

## 📬 Let's Connect

- [LinkedIn](https://www.linkedin.com/in/rrembert)  
- [Twitter](https://twitter.com/RichardDRembert)

---

## 📄 License

MIT

