
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
from io import BytesIO

st.set_page_config(page_title="Flight School Dashboard", layout="wide")

st.title("✈️ Flight School Dashboard")
st.write("Upload a flight log PDF to generate metrics and insights.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_flight_log(text):
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{4})\s+([\w\s]+)?\s*(Rental|Non Revenue|Other)?\s*\+([\d\.]+)?\s*(?!Hobbs Total)\d*\.?\d*\s*\+([\d\.]+)?\s*(\d*\.?\d*)"
    )
    matches = pattern.findall(text)

    data = []
    for match in matches:
        date, pilot, ftype, hobbs, tach, tach_total = match
        if hobbs:
            data.append({
                "Date": date,
                "Pilot": pilot.strip() if pilot else "Unknown",
                "Type": ftype.strip() if ftype else "Unknown",
                "Hobbs Hours": float(hobbs) if hobbs else 0,
                "Tach Hours": float(tach) if tach else 0,
                "Tach Total": float(tach_total) if tach_total else 0,
            })
    return pd.DataFrame(data)

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    df = parse_flight_log(text)

    if df.empty:
        st.error("No flight log data found in the uploaded PDF.")
    else:
        st.success("Flight log data extracted successfully!")
        st.dataframe(df)

        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        st.subheader("📊 Metrics Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Hobbs Hours", round(df["Hobbs Hours"].sum(), 2))
        col2.metric("Total Tach Hours", round(df["Tach Hours"].sum(), 2))
        col3.metric("Total Flights", len(df))

        st.subheader("📈 Hobbs and Tach Trends")
        st.line_chart(df[["Hobbs Hours", "Tach Hours"]].resample("W").sum())

        st.subheader("🧑‍✈️ Flights by Pilot")
        pilot_totals = df.groupby("Pilot")[["Hobbs Hours"]].sum()
        st.bar_chart(pilot_totals)

        st.subheader("📅 Monthly Breakdown")
        monthly = df.resample("M").sum()
        st.dataframe(monthly)
