import streamlit as st
import pandas as pd
from striprtf.striprtf import rtf_to_text

def convert_cell(header, value):
    """
    Convert cell value based on header:
    - Date: to datetime (%m/%d/%Y)
    - Hobbs +/- and Tach +/-: remove any '+' and convert to float.
    - Hobbs Total and Tach Total: remove commas and convert to float.
    - Pilot and Type: simply strip whitespace.
    """
    if header == "Date":
        try:
            # Convert to datetime using expected format.
            return pd.to_datetime(value, format='%m/%d/%Y', errors='coerce')
        except Exception:
            return None
    elif header in ["Hobbs +/-", "Tach +/-"]:
        try:
            return float(value.strip().lstrip('+'))
        except Exception:
            return None
    elif header in ["Hobbs Total", "Tach Total"]:
        try:
            # Remove commas and convert to float.
            return float(value.replace(',', ''))
        except Exception:
            return None
    else:
        # For Pilot and Type, just return a stripped string.
        return value.strip()

def parse_full_table(file):
    # Convert the RTF file to plain text.
    raw_text = file.read().decode("utf-8", errors="ignore")
    text = rtf_to_text(raw_text)
    
    # Split text into non-empty lines.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Define the expected headers.
    headers = ["Date", "Pilot", "Type", "Hobbs +/-", "Hobbs Total", "Tach +/-", "Tach Total"]
    
    # Check if we have enough lines.
    if len(lines) < 7:
        st.error("Not enough data to extract headers.")
        return pd.DataFrame()
    
    # We'll override the file headers with our expected headers.
    # Group every 7 lines (after the first 7 header lines) as a data row.
    data_rows = []
    for i in range(7, len(lines), 7):
        group = lines[i:i+7]
        if len(group) == 7:
            data_rows.append(group)
        else:
            # Skip incomplete rows.
            continue
    
    # Create a DataFrame with the fixed headers.
    df = pd.DataFrame(data_rows, columns=headers)
    
    # Convert each column to the proper type.
    for col in headers:
        df[col] = df[col].apply(lambda x: convert_cell(col, x))
    
    return df

st.title("Aircraft Hours Report Table")

uploaded_file = st.file_uploader("Upload Aircraft Hours Report (RTF)", type=["rtf"])

if uploaded_file is not None:
    df_table = parse_full_table(uploaded_file)
    if df_table.empty:
        st.error("No valid table data was extracted.")
    else:
        st.write("### Extracted and Cleaned Table")
        st.dataframe(df_table)
