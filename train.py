import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from joblib import dump
import os

os.makedirs("models", exist_ok=True)

# Load features
df = pd.read_csv('data/user_features.csv')
X = df[['emotion_score', 'influence_score', 'message_sentiment_score', 'emotion_risk']]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train anomaly detection model
model = IsolationForest(random_state=42, contamination=0.1)
model.fit(X_scaled)

# Save model and scaler
dump(model, "models/anomaly_model.pkl")
dump(scaler, "models/scaler.pkl")

print("[OK] Model and scaler saved in /models/")

