
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Flight School Dashboard", layout="wide")

st.title("✈️ Flight School Performance Dashboard")

# Sidebar Filters
st.sidebar.header("📊 Filter Data")
selected_year = st.sidebar.selectbox("Select Year", [2024, 2025], index=0)

# Sample metrics
st.markdown("## ✅ Metrics Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Monthly Hours", "124.6", "+5.1")
col2.metric("Aircraft Utilization", "78%", "+4%")
col3.metric("Instructor Hours", "89.2", "+2.3")

col4, col5, col6 = st.columns(3)
col4.metric("Fuel Expenses", "$9,349.98", "+$300")
col5.metric("Revenue", "$17,430", "+$1,200")
col6.metric("Revenue vs Cost Ratio", "1.86", "+0.2")

# Line chart for Hobbs/Tach hours
st.markdown("## 📈 Hobbs and Tach Trends")
sample_data = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
    'Hobbs Hours': [22, 18, 27, 35, 38, 20, 23, 26, 30, 32, 29, 25],
    'Tach Hours': [21, 17, 25, 33, 36, 19, 22, 25, 29, 31, 27, 24]
})
fig = px.line(sample_data, x='Date', y=['Hobbs Hours', 'Tach Hours'], markers=True)
st.plotly_chart(fig, use_container_width=True)

# Pie chart: Revenue by Aircraft
st.markdown("## 🛩️ Revenue by Aircraft")
rev_data = pd.DataFrame({
    'Aircraft': ['N1369F', 'N5076N', 'N8927Z'],
    'Revenue': [6500, 7300, 3630]
})
fig2 = px.pie(rev_data, values='Revenue', names='Aircraft', title='Revenue Distribution by Aircraft')
st.plotly_chart(fig2, use_container_width=True)

# Bar chart: Fuel usage
st.markdown("## ⛽ Fuel Usage by Aircraft")
fuel_data = pd.DataFrame({
    'Aircraft': ['N1369F', 'N5076N', 'N8927Z'],
    'Gallons Used': [350, 410, 200]
})
fig3 = px.bar(fuel_data, x='Aircraft', y='Gallons Used', title='Fuel Usage per Aircraft')
st.plotly_chart(fig3, use_container_width=True)

# Heatmap: Busiest Days/Hours
st.markdown("## 🔥 Busiest Flight Days/Hours (Simulated)")
heatmap_data = pd.DataFrame(
    data=[[5, 8, 10, 12, 9, 3, 1],
          [6, 10, 13, 14, 11, 5, 2],
          [4, 6, 9, 11, 10, 6, 4]],
    columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    index=["Morning", "Afternoon", "Evening"]
)
fig4, ax = plt.subplots()
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
st.pyplot(fig4)

# Tables
st.markdown("## 📋 Flight Log")
st.dataframe(sample_data.rename(columns={"Date": "Flight Date"}))

st.markdown("## 💵 Monthly Revenue Breakdown")
monthly_rev = pd.DataFrame({
    "Month": sample_data['Date'].dt.strftime('%B'),
    "Revenue": [1200, 1300, 1400, 1500, 1600, 1400, 1350, 1450, 1550, 1650, 1750, 1720]
})
st.dataframe(monthly_rev)

st.markdown("## 🧾 Maintenance Tracking (Example)")
maintenance_data = pd.DataFrame({
    "Aircraft": ["N1369F", "N5076N", "N8927Z"],
    "Last Maintenance": ["2024-01-15", "2024-02-10", "2024-03-01"],
    "Next Due": ["2024-04-15", "2024-05-10", "2024-06-01"]
})
st.dataframe(maintenance_data)

# Existing dashboard code...

# ------------------------------
# 📤 PDF Upload and Extraction Section
# ------------------------------
import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

st.header("📤 Upload Flight School PDF Data")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read PDF with PyMuPDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    st.subheader("📄 Extracted Text")
    st.text_area("PDF Content", text, height=300)

    # Example: Try to structure into rows (custom logic here)
    rows = [line for line in text.split("\n") if line.strip()]
    df = pd.DataFrame(rows, columns=["Raw Data"])
    
    st.subheader("🧾 Raw Data Preview")
    st.dataframe(df)

