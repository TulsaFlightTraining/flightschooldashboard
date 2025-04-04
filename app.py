import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def instruction_dashboard(uploaded_file, section_title):
    if uploaded_file:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)

        # Convert columns to proper types
        df["Date"] = pd.to_datetime(df["Date"])
        df["Ground"] = pd.to_numeric(df["Ground"], errors="coerce")
        df["Flight"] = pd.to_numeric(df["Flight"], errors="coerce")

        # Optional pilot filter
        pilots = df["Pilots"].dropna().unique()
        selected_pilot = st.selectbox("Filter by Pilot (optional):", options=["All"] + list(pilots), key=section_title)
        if selected_pilot != "All":
            df = df[df["Pilots"] == selected_pilot]

        # Group by date and sum hours
        daily_hours = df.groupby("Date")[["Ground", "Flight"]].sum().sort_index()
        daily_hours["Total"] = daily_hours["Ground"] + daily_hours["Flight"]

        # Cumulative hours
        cumulative_hours = daily_hours.cumsum()

        # Compute average and total for past 3 weeks
        end_date = pd.Timestamp(datetime.today().date())
        start_date = end_date - timedelta(weeks=3)
        full_range = pd.date_range(start=start_date, end=end_date)
        full_range_df = pd.DataFrame(index=full_range)
        merged = full_range_df.join(daily_hours["Total"], how="left").fillna(0)
        three_week_avg = merged["Total"].mean()
        three_week_total = merged["Total"].sum()

        # Summary stats
        st.subheader("Summary Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ground", f"{daily_hours['Ground'].sum():.2f} hrs")
        col2.metric("Total Flight", f"{daily_hours['Flight'].sum():.2f} hrs")
        col3.metric("Total Instruction", f"{daily_hours['Total'].sum():.2f} hrs")

        col4, col5 = st.columns(2)
        col4.metric("3-Week Avg (Total)", f"{three_week_avg:.2f} hrs/day")
        col5.metric("3-Week Total", f"{three_week_total:.2f} hrs")

        # Display the raw table (optional)
        st.subheader("Summed Daily Hours")
        st.dataframe(daily_hours)

        # Line chart: Daily Hours
        st.subheader("Instruction Hours Over Time")
        fig1, ax1 = plt.subplots()
        ax1.plot(daily_hours.index, daily_hours["Ground"], label="Ground Hours", marker='o')
        ax1.plot(daily_hours.index, daily_hours["Flight"], label="Flight Hours", marker='o')
        ax1.axhline(y=three_week_avg, color='red', linestyle='--', label='3-Week Avg')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Hours")
        ax1.set_title("Daily Flight and Ground Instruction Hours")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

        # Line chart: Cumulative Hours
        st.subheader("Cumulative Instruction Hours")
        fig2, ax2 = plt.subplots()
        ax2.plot(cumulative_hours.index, cumulative_hours["Ground"], label="Cumulative Ground", linestyle='--')
        ax2.plot(cumulative_hours.index, cumulative_hours["Flight"], label="Cumulative Flight", linestyle='--')
        ax2.plot(cumulative_hours.index, cumulative_hours["Total"], label="Total Instruction", linewidth=2)
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Cumulative Hours")
        ax2.set_title("Running Total of Instruction Hours")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

st.title("Flight Instruction Hours Tracker - Multi Instructor View")

instructors = [
    "Parker Foreman",
    "Abcde Bonifacio",
    "Whitt Fletcher",
    "Bobby Emert",
    "Sia Harrington",
    "Edgar Amezcua",
    "Jordan Raley",
    "(Extra Slot)"
]

for instructor in instructors:
    with st.expander(f"{instructor}"):
        uploaded = st.file_uploader(f"Upload report for {instructor}", type="csv", key=f"file_uploader_{instructor}")
        instruction_dashboard(uploaded, f"{instructor} Report")
