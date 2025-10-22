import streamlit as st
import requests
import sqlite3
import pandas as pd

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/log_water"

# Streamlit Page Config
st.set_page_config(page_title="💧 AI Water Tracker", layout="centered")

st.title("💧 AI Water Intake Tracker")
st.write("Track your daily water intake and get AI-powered hydration insights!")

# Input form
with st.form("water_form"):
    user_id = st.text_input("Enter your name (optional)", value="maheen")
    amount_ml = st.number_input("Enter water intake (ml):", min_value=100, step=100)
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {"user_id": user_id, "amount_ml": amount_ml}
        with st.spinner("Analyzing hydration data..."):
            response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            st.success(" Insight generated successfully!")
            st.info(result["message"])
        else:
            st.error("Failed to get AI insight. Check backend connection.")

# Divider
st.markdown("---")

# Display stored hydration logs
st.subheader("Hydration History")

# Connect to SQLite and show recent logs
try:
    conn = sqlite3.connect("water_tracker.db")
    df = pd.read_sql_query("SELECT * FROM water_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df)
    conn.close()
except Exception as e:
    st.error(f"Error reading database: {e}")
