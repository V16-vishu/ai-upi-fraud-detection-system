import os
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

model_path = os.path.join(os.path.dirname(__file__), "..", "models", "fraud_model.pkl")
model = joblib.load(os.path.abspath(model_path))

st.set_page_config(page_title="UPI Fraud Detection", page_icon="💳", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #020617, #0f172a, #111827);
    color: white;
}
.big-title {
    text-align:center;
    font-size:45px;
    font-weight:800;
    color:#38bdf8;
    animation: glow 1.5s infinite alternate;
}
@keyframes glow {
    from {text-shadow:0 0 10px #38bdf8;}
    to {text-shadow:0 0 30px #22d3ee;}
}
.box {
    background:#111827;
    padding:22px;
    border-radius:18px;
    border:1px solid #334155;
    box-shadow:0 0 18px rgba(56,189,248,0.25);
}
.safe {
    padding:25px;
    border-radius:18px;
    background:linear-gradient(90deg,#16a34a,#22c55e);
    font-size:28px;
    text-align:center;
    font-weight:bold;
    animation: pop 0.6s;
}
.danger {
    padding:25px;
    border-radius:18px;
    background:linear-gradient(90deg,#dc2626,#ef4444);
    font-size:28px;
    text-align:center;
    font-weight:bold;
    animation: shake 0.6s;
}
@keyframes pop {
    0% {transform:scale(0.8);}
    100% {transform:scale(1);}
}
@keyframes shake {
    0%,100% {transform:translateX(0);}
    25% {transform:translateX(-8px);}
    50% {transform:translateX(8px);}
    75% {transform:translateX(-8px);}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">💳 UPI Fraud Detection Dashboard</div>', unsafe_allow_html=True)
st.write("### AI-based fraud checker with risk score and visual analytics")

tab1, tab2 = st.tabs(["🚨 Fraud Checker", "📊 Dashboard"])

with tab1:
    st.subheader("Enter Transaction Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        amount = st.number_input("💰 Transaction Amount (INR)", min_value=0, value=5000)

    with col2:
        hour = st.slider("⏰ Hour of Day", 0, 23, 12)

    with col3:
        is_weekend = st.selectbox("📅 Weekend Transaction?", [0, 1])

    risk_score = 0

    if amount > 50000:
        risk_score += 50
    elif amount > 20000:
        risk_score += 35
    elif amount > 5000:
        risk_score += 20

    if hour >= 22 or hour <= 5:
        risk_score += 25

    if is_weekend == 1:
        risk_score += 15

    risk_score = min(risk_score, 100)

    sample = pd.DataFrame({
        'amount_(inr)': [amount],
        'hour_of_day': [hour],
        'is_weekend': [is_weekend]
    })

    if st.button("🚀 Predict Fraud Risk"):
        prediction = model.predict(sample)[0]

        if risk_score >= 60 or prediction == 1:
            st.markdown('<div class="danger">🚨 High Risk / Fraud Transaction</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="safe">✅ Normal Transaction</div>', unsafe_allow_html=True)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={'text': "Fraud Risk Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 40], 'color': "green"},
                    {'range': [40, 70], 'color': "orange"},
                    {'range': [70, 100], 'color': "red"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.write("### Reason")
        if amount > 5000:
            st.write("⚠️ High transaction amount")
        if hour >= 22 or hour <= 5:
            st.write("⚠️ Late night transaction")
        if is_weekend == 1:
            st.write("⚠️ Weekend transaction")
        if risk_score < 40:
            st.write("✅ Low risk behavior found")

with tab2:
    st.subheader("Sample Fraud Analytics Dashboard")

    data = pd.DataFrame({
        "Category": ["Shopping", "Food", "Travel", "Bills", "Recharge"],
        "Transactions": [120, 90, 60, 75, 110],
        "Fraud_Count": [18, 8, 15, 5, 10]
    })

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", "455")
    col2.metric("Fraud Transactions", "56")
    col3.metric("Fraud Rate", "12.3%")

    fig1 = px.bar(data, x="Category", y="Transactions", title="Category-wise Transactions")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(data, names="Category", values="Fraud_Count", title="Fraud by Category")
    st.plotly_chart(fig2, use_container_width=True)

    hour_data = pd.DataFrame({
        "Hour": list(range(24)),
        "Fraud_Count": [2,3,5,6,4,3,1,1,2,3,4,5,4,3,2,3,4,5,7,9,12,15,18,20]
    })

    fig3 = px.line(hour_data, x="Hour", y="Fraud_Count", title="Fraud Trend by Hour")
    st.plotly_chart(fig3, use_container_width=True)