import streamlit as st
import requests
import sqlite3
import pandas as pd
import datetime

# ------------------ CONFIG ------------------
API_URL = "http://0.0.0.0:8000/log_water"
DB_PATH = "water_tracker.db"
DAILY_GOAL = 2500  # ml

st.set_page_config(
    page_title="💧 AI Water Tracker",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Settings")

# Theme switch
theme = st.sidebar.radio("Theme", ["Light 🌞", "Dark 🌙"])
if theme == "Dark 🌙":
    st.markdown(
        """
        <style>
        body {background-color: #0E1117; color: white;}
        .stDataFrame, .stTextInput, .stNumberInput, .stButton, .stProgress {background-color: #1E1E1E;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Date filter
st.sidebar.subheader("📅 Filter Logs by Date")
start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# ------------------ MAIN TITLE ------------------
st.title("💧 AI Water Intake Tracker")
st.write("Track your daily water intake and get AI-powered hydration insights!")

# ------------------ INPUT FORM ------------------
with st.form("water_form"):
    user_id = st.text_input("👤 Enter your name:", value="maheen")
    amount_ml = st.number_input("💦 Enter water intake (ml):", min_value=100, step=100)
    submitted = st.form_submit_button("Submit Intake")

    if submitted:
        data = {"user_id": user_id, "amount_ml": amount_ml}
        with st.spinner("Analyzing your hydration..."):
            response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Insight generated successfully!")
            st.info(result["message"])
        else:
            st.error("⚠️ Could not connect to FastAPI backend.")

# ------------------ DATABASE CONNECTION ------------------
def get_logs(start_date, end_date):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT * FROM water_logs
        WHERE DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY timestamp DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ------------------ DISPLAY LOGS ------------------
st.markdown("---")
st.subheader("📊 Hydration History")

try:
    df = get_logs(start_date, end_date)
    if not df.empty:
        # Convert timestamp
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date

        # Display table
        st.dataframe(df[["id", "user_id", "amount_ml", "ai_insight", "timestamp"]])

        # ------------------ DAILY GOAL TRACKER ------------------
        total_today = df[df["date"] == datetime.date.today()]["amount_ml"].sum()
        st.subheader(f"🎯 Today's Progress ({total_today:.0f} ml / {DAILY_GOAL} ml)")
        st.progress(min(total_today / DAILY_GOAL, 1.0))

        # ------------------ CHARTS ------------------
        st.markdown("### 📈 Water Intake Over Time")
        daily_sum = df.groupby("date")["amount_ml"].sum().reset_index()
        st.line_chart(daily_sum, x="date", y="amount_ml")

        # ------------------ EXPORT OPTIONS ------------------
        st.markdown("### 📤 Export Your Data")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📁 Download CSV",
            data=csv,
            file_name="hydration_logs.csv",
            mime="text/csv",
        )

        # Export to PDF (simple text-based)
        import tempfile
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "Hydration Report", ln=True, align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i, row in df.iterrows():
            pdf.multi_cell(0, 10, f"{row['timestamp']} - {row['amount_ml']}ml - {row['ai_insight']}")
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_pdf.name)
        with open(temp_pdf.name, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name="hydration_report.pdf",
                mime="application/pdf",
            )
    else:
        st.info("No logs found for the selected date range.")
except Exception as e:
    st.error(f"Error loading data: {e}")
