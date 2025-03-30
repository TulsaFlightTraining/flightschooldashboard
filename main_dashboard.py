import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Dummy Parsing Functions
# -------------------------------

# Parsing function for Instructor Reports.
def parse_pdf_instructor(file):
    # Replace this dummy data with your actual PDF/RTF parsing logic.
    data = [
        {"Date": "2025-03-29", "Instructor": "Parker Foreman", "Flight": 1.5, "Ground": 1.0},
        {"Date": "2025-03-28", "Instructor": "Parker Foreman", "Flight": 1.2, "Ground": 0.8},
        {"Date": "2025-03-27", "Instructor": "Parker Foreman", "Flight": 1.5, "Ground": 0.0},
        {"Date": "2025-03-29", "Instructor": "Whitt Fletcher", "Flight": 1.0, "Ground": 0.5},
        {"Date": "2025-03-27", "Instructor": "Edgar Amezcua", "Flight": 1.3, "Ground": 0.7},
        # Add additional rows as needed.
    ]
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Parsing function for Aircraft Hours Reports.
def parse_pdf_aircraft_hours(file):
    # Replace this dummy data with your actual PDF/RTF parsing logic.
    data = [
        {"Date": "03/29/2025", "Pilot": "Derek Smith", "Type": "Rental", "HobbsDelta": 2.50},
        {"Date": "03/29/2025", "Pilot": "Discovery flight", "Type": "Rental", "HobbsDelta": 0.70},
        {"Date": "03/27/2025", "Pilot": "Derek Smith", "Type": "Rental", "HobbsDelta": 1.20},
        {"Date": "03/27/2025", "Pilot": "Sawyer Gepford", "Type": "Rental", "HobbsDelta": 1.00},
        {"Date": "03/27/2025", "Pilot": "Travis Linville", "Type": "Rental", "HobbsDelta": 2.70},
        # Add additional rows as needed.
    ]
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
    return df

# -------------------------------
# Streamlit Dashboard Layout
# -------------------------------

st.title("Flight School Dashboard")

# -------------------------------
# Instructor Reports Upload Section
# -------------------------------
st.header("Instructor Reports Upload")
instructor_file = st.file_uploader("Upload Instructor Report (PDF/RTF)", type=["pdf", "rtf"], key="instructor")

if instructor_file is not None:
    df_instructors = parse_pdf_instructor(instructor_file)
    st.write("### Parsed Instructor Data")
    st.dataframe(df_instructors)
    
    # List of all instructors in the system.
    instructors_list = [
        "Whitt Fletcher", "Abcde Bonifacio", "Parker Foreman",
        "Edgar Amezcua", "Bobby Emert", "Jordan Raley",
        "Riley King", "Sia Harrington"
    ]
    
    # Define the current date as the report run date and compute the 21-day window.
    current_date = datetime.now()
    start_date = current_date - timedelta(days=21)
    
    # Filter data to only include the past 21 days.
    df_filtered = df_instructors[(df_instructors['Date'] >= start_date) & (df_instructors['Date'] <= current_date)]
    
    results = []
    for instructor in instructors_list:
        df_instr = df_filtered[df_filtered['Instructor'] == instructor].copy()
        # Calculate combined hours (Flight + Ground) for each session.
        df_instr['Total Hours'] = df_instr['Flight'] + df_instr['Ground']
        total_hours = df_instr['Total Hours'].sum()
        # Divide by 21 days to include days with no work.
        avg_daily = total_hours / 21
        results.append({
            "Instructor": instructor,
            "3-Week Average Work Hours (per day)": round(avg_daily, 2)
        })
    
    results_df = pd.DataFrame(results)
    st.write("### Instructor 3‑Week Average Work Hours")
    st.dataframe(results_df)

# -------------------------------
# Aircraft Hours Reports Upload Section
# -------------------------------
st.header("Aircraft Hours Reports Upload")
aircraft_file = st.file_uploader("Upload Aircraft Hours Report (PDF/RTF)", type=["pdf", "rtf"], key="aircraft")

if aircraft_file is not None:
    df_aircraft = parse_pdf_aircraft_hours(aircraft_file)
    st.write("### Parsed Aircraft Hours Data")
    st.dataframe(df_aircraft)
    
    # Sum up the total incremental hours from the HobbsDelta column only.
    total_hobbs_hours = df_aircraft["HobbsDelta"].sum()
    
    st.write("### Aircraft Hours Summary")
    st.write(f"Total Aircraft Hours (Hobbs +/-): {total_hobbs_hours:.2f}")
