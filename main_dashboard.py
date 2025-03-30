import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Parsing Functions Using striprtf for RTF files
# -------------------------------
def parse_pdf_instructor(file):
    # If the file is an RTF, use striprtf to convert it to text.
    if file.name.lower().endswith(".rtf"):
        from striprtf.striprtf import rtf_to_text
        raw_text = file.read().decode("utf-8", errors="ignore")
        text = rtf_to_text(raw_text)
        rows = []
        # Assume that each line that starts with a date (e.g., "Mar") is a row.
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("Date"):
                continue
            # Expecting a line like:
            # "Mar 29, 2025   Braylen Dillard   $50.00   1.5   0.0   $75.00"
            parts = line.split()
            try:
                # Combine the first three parts to form the date (e.g., "Mar 29, 2025")
                date_str = " ".join(parts[:3])
                date_val = datetime.strptime(date_str, "%b %d, %Y")
            except Exception:
                continue
            try:
                # For simplicity, assume "Ground" is at index 5 and "Flight" is at index 6.
                ground = float(parts[5])
                flight = float(parts[6])
            except Exception:
                continue
            # Determine instructor from the file name; if "parker" is in the name, assume Parker Foreman.
            instructor = "Parker Foreman" if "parker" in file.name.lower() else "Unknown Instructor"
            rows.append({"Date": date_val, "Instructor": instructor, "Flight": flight, "Ground": ground})
        # Ensure we return a DataFrame with the expected columns.
        if not rows:
            return pd.DataFrame(columns=["Date", "Instructor", "Flight", "Ground"])
        return pd.DataFrame(rows)
    else:
        # Fallback dummy data for non-RTF uploads.
        data = [
            {"Date": "2025-03-29", "Instructor": "Parker Foreman", "Flight": 1.5, "Ground": 1.0},
            {"Date": "2025-03-28", "Instructor": "Parker Foreman", "Flight": 1.2, "Ground": 0.8},
            {"Date": "2025-03-27", "Instructor": "Parker Foreman", "Flight": 1.5, "Ground": 0.0},
        ]
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

def parse_pdf_aircraft_hours(file):
    # If the file is an RTF, use striprtf to convert it to text.
    if file.name.lower().endswith(".rtf"):
        from striprtf.striprtf import rtf_to_text
        raw_text = file.read().decode("utf-8", errors="ignore")
        text = rtf_to_text(raw_text)
        rows = []
        # Process each line to extract rows with a date and a HobbsDelta value.
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("Date"):
                continue
            # Expecting a line format like:
            # "03/29/2025   Derek Smith   Rental   +2.50   6,017.80   +1.90   3,702.47"
            parts = line.split()
            try:
                date_val = datetime.strptime(parts[0], "%m/%d/%Y")
            except Exception:
                continue
            try:
                hobbs_str = parts[3]
                hobbs_val = float(hobbs_str.lstrip('+'))
            except Exception:
                continue
            rows.append({"Date": date_val, "HobbsDelta": hobbs_val})
        if not rows:
            return pd.DataFrame(columns=["Date", "HobbsDelta"])
        return pd.DataFrame(rows)
    else:
        # Fallback dummy data for non-RTF uploads.
        data = [
            {"Date": "03/29/2025", "Pilot": "Derek Smith", "Type": "Rental", "HobbsDelta": 2.50},
            {"Date": "03/29/2025", "Pilot": "Discovery flight", "Type": "Rental", "HobbsDelta": 0.70},
            {"Date": "03/27/2025", "Pilot": "Derek Smith", "Type": "Rental", "HobbsDelta": 1.20},
            {"Date": "03/27/2025", "Pilot": "Sawyer Gepford", "Type": "Rental", "HobbsDelta": 1.00},
            {"Date": "03/27/2025", "Pilot": "Travis Linville", "Type": "Rental", "HobbsDelta": 2.70},
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
    # Debug: Show columns to help identify issues.
    st.write("Parsed columns:", df_instructors.columns.tolist())
    if df_instructors.empty or "Date" not in df_instructors.columns:
        st.error("No valid instructor data was parsed from the file.")
    else:
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
        
        try:
            df_filtered = df_instructors[(df_instructors['Date'] >= start_date) & (df_instructors['Date'] <= current_date)]
        except Exception as e:
            st.error(f"Error filtering instructor data by date: {e}")
            df_filtered = pd.DataFrame()
        
        results = []
        for instructor in instructors_list:
            df_instr = df_filtered[df_filtered['Instructor'] == instructor].copy()
            if not df_instr.empty:
                # Calculate combined hours (Flight + Ground) for each session.
                df_instr['Total Hours'] = df_instr['Flight'] + df_instr['Ground']
            else:
                df_instr['Total Hours'] = 0
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
    st.write("Parsed columns:", df_aircraft.columns.tolist())
    if df_aircraft.empty or "HobbsDelta" not in df_aircraft.columns:
        st.error("No valid aircraft hours data was parsed from the file.")
    else:
        st.write("### Parsed Aircraft Hours Data")
        st.dataframe(df_aircraft)
        
        # Sum up the total incremental hours from the HobbsDelta column only.
        try:
            total_hobbs_hours = df_aircraft["HobbsDelta"].sum()
            st.write("### Aircraft Hours Summary")
            st.write(f"Total Aircraft Hours (Hobbs +/-): {total_hobbs_hours:.2f}")
        except Exception as e:
            st.error(f"Error calculating aircraft hours: {e}")
