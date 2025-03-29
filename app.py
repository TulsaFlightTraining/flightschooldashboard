
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import fitz  # PyMuPDF

st.set_page_config(page_title="Flight School Dashboard", layout="wide")

st.title("🛩️ Flight School Dashboard")

# Sidebar for file upload
st.sidebar.header("Upload PDF")
pdf_file = st.sidebar.file_uploader("Upload a PDF with flight data", type=["pdf"])

if pdf_file:
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    st.subheader("📄 Extracted Text from PDF")
    st.text_area("Raw Text", text, height=300)

    # Optional: show table of lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    df_raw = pd.DataFrame(lines, columns=["Extracted Line"])
    st.subheader("📝 Extracted Raw Data (Line-by-Line)")
    st.dataframe(df_raw, use_container_width=True)

# Sample dashboard metrics
st.markdown("### ✅ Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Hobbs Hours (Monthly)", "87.5", "+12.4")
col2.metric("Aircraft Utilization %", "76%", "-3%")
col3.metric("Instructor Hours", "42", "+8")

# Sample line graph for Hobbs Hours
st.markdown("### 📈 Hobbs Hours Over Time")
sample_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Hours": [40, 55, 60, 70, 87.5]
})
fig, ax = plt.subplots()
ax.plot(sample_data["Month"], sample_data["Hours"], marker='o')
ax.set_title("Monthly Hobbs Hours")
ax.set_ylabel("Hours")
ax.set_xlabel("Month")
st.pyplot(fig)

# Sample table
st.markdown("### 📊 Recent Flight Log")
log_data = pd.DataFrame({
    "Date": ["2024-03-01", "2024-03-02", "2024-03-03"],
    "Pilot": ["John", "Jane", "Jim"],
    "Hours": [2.5, 3.0, 4.1],
    "Aircraft": ["N123AB", "N234BC", "N345CD"]
})
st.dataframe(log_data, use_container_width=True)
