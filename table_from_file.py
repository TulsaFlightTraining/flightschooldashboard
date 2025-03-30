import streamlit as st
import pandas as pd
from striprtf.striprtf import rtf_to_text

def parse_full_table(file):
    # Convert the RTF file content to plain text.
    raw_text = file.read().decode("utf-8", errors="ignore")
    text = rtf_to_text(raw_text)
    
    # Split text into non-empty, stripped lines.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Expected headers
    expected_headers = ["Date", "Pilot", "Type", "Hobbs +/-", "Hobbs Total", "Tach +/-", "Tach Total"]
    
    if len(lines) < 7:
        st.error("Not enough data to extract headers.")
        return pd.DataFrame()
    
    # Use the expected headers regardless of what's in the file.
    headers = expected_headers
    
    # Now, every 7 lines after the headers represent a row.
    data_rows = []
    # Start from index 7 (after headers) and step by 7.
    for i in range(7, len(lines), 7):
        group = lines[i:i+7]
        if len(group) == 7:
            data_rows.append(group)
        else:
            # Skip incomplete groups
            continue
    
    # Create DataFrame from the extracted rows.
    df = pd.DataFrame(data_rows, columns=headers)
    return df

st.title("Aircraft Hours Report Table")

uploaded_file = st.file_uploader("Upload Aircraft Hours Report (RTF)", type=["rtf"])

if uploaded_file is not None:
    df_table = parse_full_table(uploaded_file)
    if df_table.empty:
        st.error("No valid table data was extracted.")
    else:
        st.write("### Extracted Table")
        st.dataframe(df_table)
