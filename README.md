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
- **Modeling**: TensorFlow or PyTorch
- **Notebook Interface**: Jupyter
- **Visualization**: Matplotlib, Seaborn, SHAP
- **Data**: [Formula 1 telemetry & race data](https://ergast.com/mrd/), FastF1, or custom datasets

---

## 🧠 Core Features

- Load & preprocess telemetry and race data
- Extract features: pace vs. teammate, overtakes, lap-by-lap consistency
- Train regression/classification model for performance scoring
- Apply SHAP or attention layers to interpret model predictions
- Export driver performance dashboards (PDF/HTML)

---

## 📁 Project Structure (Coming Soon)


---

## 🚧 Roadmap

- [ ] Ingest telemetry + lap data from 2021–2024 seasons
- [ ] Feature engineering pipeline (pace, deltas, overtake rate)
- [ ] Train baseline performance scoring model
- [ ] Integrate SHAP values for explainability
- [ ] Build dashboard/visual summary per driver & race
- [ ] Package as web app or shareable notebook

---

## 🤝 Contributions Welcome

Have ideas, data sources, or visual improvements? Open an issue or submit a PR!

---

## 📬 Let's Connect

- [LinkedIn](https://www.linkedin.com/in/rrembert)
- [Twitter](https://twitter.com/RichardDRembert)

---

**License**: MIT  

