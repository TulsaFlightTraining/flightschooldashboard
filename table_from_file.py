import pandas as pd
from striprtf.striprtf import rtf_to_text

def parse_rtf_table(rtf_file_path):
    """
    Reads an RTF file, extracts plain text, and parses the text into a pandas DataFrame.
    The RTF file should have the first 7 non-empty lines as headers:
        Date, Pilot, Type, Hobbs +/-, Hobbs Total, Tach +/-, Tach Total
    Each subsequent group of 7 non-empty lines will be interpreted as one record.
    """
    # Read the RTF file content
    with open(rtf_file_path, 'r') as file:
        rtf_content = file.read()
    
    # Convert RTF to plain text
    plain_text = rtf_to_text(rtf_content)
    
    # Split the text into lines and remove empty lines
    lines = [line.strip() for line in plain_text.splitlines() if line.strip()]
    
    # Assume the first 7 lines are the header row
    header = lines[:7]
    data_lines = lines[7:]
    
    # Group the remaining lines into rows of 7 elements each
    num_columns = len(header)
    rows = [data_lines[i:i + num_columns] for i in range(0, len(data_lines), num_columns)]
    
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=header)
    return df

if __name__ == '__main__':
    # Replace 'your_file.rtf' with the path to your RTF file.
    rtf_file_path = 'your_file.rtf'
    df = parse_rtf_table(rtf_file_path)
    
    # Print the DataFrame in a neat table format.
    print(df.to_string(index=False))
