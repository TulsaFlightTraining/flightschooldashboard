
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import re
from datetime import datetime

st.set_page_config(page_title="Flight School Dashboard", layout="wide")

st.title("📊 Flight School Dashboard")
st.sidebar.header("Upload PDF Flight Log")

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_flight_log(text):
    pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(Non Revenue|Rental|Other)\s+\+(\d+\.\d+)\s+(\d+\.\d+)\s+\+(\d+\.\d+)\s+(\d+\.\d+)")
    data = pattern.findall(text)
    df = pd.DataFrame(data, columns=["Date", "Pilot", "Type", "Hobbs +", "Hobbs Total", "Tach +", "Tach Total"])
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    df[["Hobbs +", "Hobbs Total", "Tach +", "Tach Total"]] = df[["Hobbs +", "Hobbs Total", "Tach +", "Tach Total"]].astype(float)
    return df.sort_values("Date")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    df = parse_flight_log(text)

    st.subheader("📋 Flight Log Table")
    st.dataframe(df)

    st.subheader("📈 Total Hours Flown Per Month")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_hours = df.groupby("Month")["Hobbs +"].sum()
    st.line_chart(monthly_hours)

    st.subheader("📉 Weekly Hours Flown")
    df["Week"] = df["Date"].dt.strftime('%Y-%U')
    weekly_hours = df.groupby("Week")["Hobbs +"].sum()
    st.bar_chart(weekly_hours)

    st.subheader("📍 Flight Logs by Pilot")
    st.dataframe(df.groupby("Pilot")[["Hobbs +", "Tach +"]].sum().sort_values("Hobbs +", ascending=False))

    st.subheader("🛩️ Aircraft Utilization Heatmap (Sample Placeholder)")
    fig, ax = plt.subplots()
    sns.heatmap(pd.crosstab(df["Date"].dt.day_name(), df["Date"].dt.hour).fillna(0), ax=ax, cmap="Blues")
    st.pyplot(fig)
