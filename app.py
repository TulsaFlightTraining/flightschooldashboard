import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Flight Instruction Hours Tracker")

# File uploader
uploaded_file = st.file_uploader("Upload your flight instruction log (CSV)", type="csv")

if uploaded_file:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)

    # Convert columns to proper types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Ground"] = pd.to_numeric(df["Ground"], errors="coerce")
    df["Flight"] = pd.to_numeric(df["Flight"], errors="coerce")

    # Group by date and sum hours
    daily_hours = df.groupby("Date")[["Ground", "Flight"]].sum().sort_index()

    # Display the raw table (optional)
    st.subheader("Summed Daily Hours")
    st.dataframe(daily_hours)

    # Plot the line chart
    st.subheader("Instruction Hours Over Time")
    fig, ax = plt.subplots()
    ax.plot(daily_hours.index, daily_hours["Ground"], label="Ground Hours", marker='o')
    ax.plot(daily_hours.index, daily_hours["Flight"], label="Flight Hours", marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours")
    ax.set_title("Daily Flight and Ground Instruction Hours")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

