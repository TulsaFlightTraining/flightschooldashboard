import os
import pandas as pd
from striprtf.striprtf import rtf_to_text

def parse_rtf_table(rtf_file_path):
    """
    Reads an RTF file, converts it to plain text, and parses the text into a pandas DataFrame.
    The RTF file should have the first 7 non-empty lines as headers:
        Date, Pilot, Type, Hobbs +/-, Hobbs Total, Tach +/-, Tach Total
    Each subsequent group of 7 non-empty lines will be interpreted as one record.
    """
    if not os.path.exists(rtf_file_path):
        raise FileNotFoundError(f"File not found: {rtf_file_path}")
    
    # Read the RTF file content
    with open(rtf_file_path, 'r') as file:
        rtf_content = file.read()
    
    # Convert RTF to plain text
    plain_text = rtf_to_text(rtf_content)
    
    # Split the text into non-empty lines
    lines = [line.strip() for line in plain_text.splitlines() if line.strip()]
    
    # Assume the first 7 lines are header names
    header = lines[:7]
    data_lines = lines[7:]
    
    # Group the remaining lines into rows of 7 items each
    num_columns = len(header)
    rows = [data_lines[i:i + num_columns] for i in range(0, len(data_lines), num_columns)]
    
    # Create and return a DataFrame
    df = pd.DataFrame(rows, columns=header)
    return df

if __name__ == '__main__':
    # Update the path to your RTF file accordingly
    rtf_file_path = 'your_file.rtf'
    
    try:
        df = parse_rtf_table(rtf_file_path)
        # Print the DataFrame in a neatly formatted table
        print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")
