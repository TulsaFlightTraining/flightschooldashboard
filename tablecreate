import streamlit as st
import pandas as pd
from striprtf.striprtf import rtf_to_text

def parse_full_aircraft_table(file):
    # Convert the RTF file content to plain text.
    raw_text = file.read().decode("utf-8", errors="ignore")
    text = rtf_to_text(raw_text)
    
    # Split the text into non-empty lines.
    lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
    
    # Expect that the first 7 lines are the header.
    if len(lines) < 7:
        st.error("Not enough lines to extract headers.")
        return pd.DataFrame()
    
    headers = lines[:7]
    
    # Group every 7 subsequent lines as a row.
    data_rows = []
    for i in range(7, len(lines), 7):
        group = lines[i:i+7]
        if len(group) == 7:
            data_rows.append(group)
        else:
            # If the last group is incomplete, you may choose to skip it.
            pass
    
    # Create a DataFrame using the headers and data rows.
    df = pd.DataFrame(data_rows, columns=headers)
    return df

st.title("Aircraft Hours Report Table")

uploaded_file = st.file_uploader("Upload Aircraft Hours Report (RTF)", type=["rtf"])

if uploaded_file is not None:
    df_table = parse_full_aircraft_table(uploaded_file)
    if df_table.empty:
        st.error("No valid table data was extracted.")
    else:
        st.write("### Aircraft Hours Report Table")
        st.dataframe(df_table)
