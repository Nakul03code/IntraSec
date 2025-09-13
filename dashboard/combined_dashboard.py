import streamlit as st
import pandas as pd
from joblib import load
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import random
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Insider Threat Monitoring")

# Load processed data
df = pd.read_csv("data/user_features.csv")

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# Load model & scaler
model = load("models/anomaly_model.pkl")
scaler = load("models/scaler.pkl")

# Features for anomaly detection
X = df[["emotion_score", "influence_score", "message_sentiment_score", "emotion_risk"]]
X_scaled = scaler.transform(X)

# Predict anomalies
preds = model.predict(X_scaled)
df["anomaly"] = preds
df["anomaly"] = df["anomaly"].map({1: "Normal", -1: "Anomaly"})

# Risk persona assignment
def risk_persona(row):
    if row["anomaly"] == "Anomaly" and row["emotion_score"] > 0.7:
        return "High Risk"
    elif row["anomaly"] == "Anomaly":
        return "Medium Risk"
    else:
        return "Low Risk"

df["risk_persona"] = df.apply(risk_persona, axis=1)

# Explanation function
def explain_flag(row):
    reasons = []
    if row["emotion_score"] > 0.7:
        reasons.append("High emotion")
    if row["influence_score"] > 0.6:
        reasons.append("High influence")
    if row["message_sentiment_score"] > 0.9:
        reasons.append("Unusual sentiment")
    if row["anomaly"] == "Anomaly":
        reasons.append("Model flagged anomaly")
    return ", ".join(reasons)

df["explanation"] = df.apply(explain_flag, axis=1)

# Tabs (added "AI Assistant")
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "User Detail", "Collusion Graph", "Alerts", "AI Assistant"]
)

# --- Tab 1: Overview ---
with tab1:
    st.subheader("User Overview")
    st.dataframe(df)
    # (rest of overview code unchanged...)

# --- Tab 2: User Detail ---
with tab2:
    user = st.selectbox("Select user", df["user"].unique())
    st.write(df[df["user"] == user])

# --- Tab 3: Collusion Graph ---
with tab3:
    st.subheader("Graph Analysis: Collusion / Communication")
    G = nx.Graph()
    for idx, row in df.iterrows():
        other_user = random.choice(df["user"].tolist())
        if other_user != row["user"]:
            G.add_edge(row["user"], other_user, weight=row["influence_score"])

    net = Network(height="600px", width="100%")
    color_map = {"High Risk": "red", "Medium Risk": "orange", "Low Risk": "green"}
    for idx, row in df.iterrows():
        net.add_node(row["user"], color=color_map.get(row["risk_persona"], "blue"))

    net.from_nx(G)
    net.write_html("dashboard/graph.html")
    with open("dashboard/graph.html") as f:
        components.html(f.read(), height=600)

# --- Tab 4: Alerts ---
with tab4:
    st.subheader("High Risk Alerts with Explanations")
    high_risk = df[df["risk_persona"] == "High Risk"]
    if not high_risk.empty:
        st.warning(f"[ALERT] {len(high_risk)} high-risk users detected!")
        for _, row in high_risk.iterrows():
            with st.expander(f"{row['user']} - {row['risk_persona']}"):
                st.markdown(f"**Message:** {row['message']}")
                st.markdown(f"**Timestamp:** {row['timestamp']}")
                st.markdown(f"**Reason:** {row['explanation']}")
                st.markdown("---")
        st.download_button(
            "Download High-Risk Report (CSV)",
            high_risk.to_csv(index=False),
            "high_risk_report.csv",
        )
    else:
        st.success("No high-risk users detected.")

# --- Tab 5: AI Assistant ---
with tab5:
    st.subheader("Intrasec AI Assistant")
    try:
        with open("dashboard/assistant.html") as f:
            components.html(f.read(), height=800, scrolling=True)
    except FileNotFoundError:
        st.error("assistant.html not found in dashboard/ directory.")
