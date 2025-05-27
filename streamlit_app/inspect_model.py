import joblib

model = joblib.load("models/driver_score_model.pkl")
print("✅ Model expects these features:")
print(model.feature_names_in_)
