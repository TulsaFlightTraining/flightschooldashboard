
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("✈️ Flight School Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload Flight Log PDF", type=["pdf"])

def parse_flight_log_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    # Extract relevant flight log entries using regex
    pattern = r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(Rental|Non Revenue|Other)\s+\+(\d+\.\d{2})\s+\d+\.\d{2}\s+\+(\d+\.\d{2})\s+(\d+\.\d{2})"
    matches = re.findall(pattern, text)

    # Convert to DataFrame
    data = []
    for match in matches:
        date, pilot, flight_type, hobbs_delta, tach_delta, tach_total = match
        data.append({
            "Date": pd.to_datetime(date),
            "Pilot": pilot.strip(),
            "Type": flight_type,
            "Hobbs Hours": float(hobbs_delta),
            "Tach Hours": float(tach_delta),
            "Tach Total": float(tach_total),
        })

    df = pd.DataFrame(data)
    return df

if uploaded_file:
    try:
        df = parse_flight_log_pdf(uploaded_file)
        st.success("Flight log data parsed successfully!")

        # Display raw data
        st.subheader("📋 Raw Flight Log Data")
        st.dataframe(df)

        # Metrics
        st.subheader("📊 Metrics")
        total_hours_month = df[df["Date"] >= pd.Timestamp.now() - pd.DateOffset(months=1)]["Hobbs Hours"].sum()
        total_hours_week = df[df["Date"] >= pd.Timestamp.now() - pd.DateOffset(weeks=1)]["Hobbs Hours"].sum()
        instructor_hours = df[df["Type"] == "Non Revenue"]["Hobbs Hours"].sum()
        revenue_hours = df[df["Type"] == "Rental"]["Hobbs Hours"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Hours (Month)", f"{total_hours_month:.1f}")
        col2.metric("Total Hours (Week)", f"{total_hours_week:.1f}")
        col3.metric("Instructor Hours", f"{instructor_hours:.1f}")
        col4.metric("Revenue Hours", f"{revenue_hours:.1f}")

        # Charts
        st.subheader("📈 Charts")

        df["Month"] = df["Date"].dt.to_period("M")
        monthly = df.groupby("Month")["Hobbs Hours"].sum().reset_index()
        monthly["Month"] = monthly["Month"].astype(str)

        st.line_chart(monthly.set_index("Month"))

        pie_data = df.groupby("Pilot")["Hobbs Hours"].sum()
        st.subheader("Revenue by Pilot")
        st.pyplot(pie_data.plot.pie(autopct="%1.1f%%", figsize=(6, 6), title="Hobbs Hours by Pilot").get_figure())

    except Exception as e:
        st.error(f"Failed to parse flight log: {e}")
