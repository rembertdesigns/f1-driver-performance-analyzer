import streamlit as st
import pandas as pd
import joblib
import shap
import streamlit.components.v1 as components

# Load model
model = joblib.load("models/driver_score_model.pkl")

# Sample driver data
driver_data = {
    "Hamilton": [0.42, 0.29],
    "Verstappen": [0.78, 0.22],
    "Leclerc": [0.30, 0.35],
    "Alonso": [0.52, 0.40],
    "Norris": [0.41, 0.26],
}

drivers = list(driver_data.keys())
features = ["pace_delta_vs_teammate", "lap_time_std_dev"]

# --- UI
st.set_page_config(page_title="F1 Driver Analyzer", layout="wide")
st.sidebar.title("🏁 F1 Driver Selector")
selected_driver = st.sidebar.selectbox("Choose a driver", drivers)

st.title("🏎️ F1 Driver Performance Analyzer")
st.caption("Powered by AI + real telemetry data")

# --- Prediction
X = pd.DataFrame([driver_data[selected_driver]], columns=features)
prediction = model.predict(X)[0]

# --- Display Results
st.metric("🏆 Predicted Score", f"{prediction:.2f}")
st.write("### 📊 Driver Feature Vector")
st.dataframe(X)

# --- SHAP Force Plot (safe for Streamlit)
st.write("### 🔍 SHAP Force Plot Explanation")

explainer = shap.Explainer(model, X)
shap_values = explainer(X)

# Render JS-based SHAP force plot
shap_html = shap.plots.force(shap_values[0], matplotlib=False)
components.html(shap.getjs() + shap_html.html(), height=400, scrolling=True)

 # Clear to prevent reuse on next render




