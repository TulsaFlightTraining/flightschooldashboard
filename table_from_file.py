import streamlit as st
import pandas as pd
from striprtf.striprtf import rtf_to_text

def parse_table(file):
    # Read the RTF file and convert it to plain text.
    raw_text = file.read().decode("utf-8", errors="ignore")
    text = rtf_to_text(raw_text)
    
    # Split into non-empty, stripped lines.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Define the fixed headers.
    headers = ["Date", "Pilot", "Type", "Hobbs +/-", "Hobbs Total", "Tach +/-", "Tach Total"]
    
    # If the file contains headers, they should be the first 7 lines.
    # Check if the first 7 lines match our expected headers (ignoring case).
    if len(lines) >= 7:
        first_seven = lines[:7]
        if all(a.lower() == b.lower() for a, b in zip(first_seven, headers)):
            data_lines = lines[7:]
        else:
            # If the first 7 lines do not match, assume there are no headers in the file.
            data_lines = lines
    else:
        st.error("The file does not have enough lines to extract headers and data.")
        return pd.DataFrame()
    
    # Group the data lines into rows of 7.
    rows = []
    for i in range(0, len(data_lines), 7):
        group = data_lines[i:i+7]
        if len(group) == 7:
            rows.append(group)
    return pd.DataFrame(rows, columns=headers)

def clean_dataframe(df):
    # Convert the Date column to datetime.
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
    
    # For Pilot and Type, strip any extra whitespace.
    df["Pilot"] = df["Pilot"].str.strip()
    df["Type"] = df["Type"].str.strip()
    
    # For the numeric columns:
    # Remove any '+' symbols and commas, then convert to float.
    for col in ["Hobbs +/-", "Tach +/-"]:
        df[col] = df[col].str.replace('+', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["Hobbs Total", "Tach Total"]:
        df[col] = df[col].str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

st.title("Aircraft Hours Report Table")

uploaded_file = st.file_uploader("Upload Aircraft Hours Report (RTF)", type=["rtf"])

if uploaded_file is not None:
    df_raw = parse_table(uploaded_file)
    if df_raw.empty:
        st.error("No valid data could be extracted from the file.")
    else:
        df_clean = clean_dataframe(df_raw)
        st.write("### Extracted and Cleaned Table")
        st.dataframe(df_clean)
