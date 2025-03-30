
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import io
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Flight School Dashboard")

st.title("📊 Flight School Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload Flight Log PDF", type=["pdf"])

def extract_flight_data_from_text(text):
    pattern = r"(\d{2}/\d{2}/\d{4})\s+([A-Za-z ]+)\s+(Non Revenue|Rental|Other)\s+\+(\d+\.\d+)\s+(\d+\.\d+)\s+\+(\d+\.\d+)\s+(\d+\.\d+)"
    matches = re.findall(pattern, text)
    if not matches:
        return pd.DataFrame()
    data = []
    for m in matches:
        data.append({
            "Date": pd.to_datetime(m[0], format="%m/%d/%Y"),
            "Pilot": m[1].strip(),
            "Type": m[2],
            "Hobbs +/-": float(m[3]),
            "Hobbs Total": float(m[4]),
            "Tach +/-": float(m[5]),
            "Tach Total": float(m[6]),
        })
    return pd.DataFrame(data)

if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    df = extract_flight_data_from_text(text)

    if not df.empty:
        st.subheader("Flight Log Data")
        st.dataframe(df)

        st.subheader("Metrics Dashboard")

        df["Month"] = df["Date"].dt.to_period("M")
        monthly_hours = df.groupby("Month")["Hobbs +/-"].sum()
        weekly_hours = df.set_index("Date").resample("W")["Hobbs +/-"].sum()

        col1, col2 = st.columns(2)
        col1.metric("Total Hours Flown (Monthly Avg)", f"{monthly_hours.mean():.2f}")
        col2.metric("Total Hours Flown (Weekly Avg)", f"{weekly_hours.mean():.2f}")

        st.subheader("📈 Hobbs Hour Trend")
        fig, ax = plt.subplots()
        df_sorted = df.sort_values("Date")
        ax.plot(df_sorted["Date"], df_sorted["Hobbs Total"], marker="o")
        ax.set_title("Hobbs Total Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Hobbs Total")
        st.pyplot(fig)

    else:
        st.warning("No flight log data detected in the uploaded PDF.")
