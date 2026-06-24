import streamlit as st
import pandas as pd
import plotly.express as px
from docx import Document
import io
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Borehole Management", layout="wide", page_icon="🚰")
st.title("🚰 Water Supply & Borehole Management Web App")

# 2. Initialize Session State for Data Storage
if "daily_data" not in st.session_state:
    st.session_state.daily_data = pd.DataFrame([
        {"Date": "2026-06-20", "Borehole": "Dhamuug Main", "Engine1_Hours": 8.0, "Engine2_Hours": 4.0, "Production_m3": 120, "Diesel_Liters": 15},
        {"Date": "2026-06-21", "Borehole": "Afraag Main Station", "Engine1_Hours": 6.5, "Engine2_Hours": 5.0, "Production_m3": 95, "Diesel_Liters": 12},
        {"Date": "2026-06-22", "Borehole": "Dhamuug Main", "Engine1_Hours": 7.0, "Engine2_Hours": 6.0, "Production_m3": 110, "Diesel_Liters": 14}
    ])

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Charts", "📝 Daily Entry Form", "📄 Export Reports"])

# ==================== TAB 1: DASHBOARD & CHARTS ====================
with tab1:
    st.header("Borehole Performance & KPIs")
    df = pd.DataFrame(st.session_state.daily_data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Production (m³)", f"{df['Production_m3'].sum():,}")
    col2.metric("Total Diesel Used (Liters)", f"{df['Diesel_Liters'].sum():,}")
    col3.metric("Total Engine 1 Hours", f"{df['Engine1_Hours'].sum():,}")
    
    st.subheader("Production per Borehole")
    fig = px.bar(df, x="Date", y="Production_m3", color="Borehole", barmode="group", title="Daily Water Production (m³)")
    st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 2: DAILY ENTRY ====================
with tab2:
    st.header("Daily Data Input Form")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("Date", datetime.now())
            borehole = st.selectbox("Select Borehole", ["Dhamuug Main", "Afraag Main Station"])
            e1_hours = st.number_input("Engine 1 Hours", min_value=0.0, step=0.5)
            e2_hours = st.number_input("Engine 2 Hours", min_value=0.0, step=0.5)
        with col2:
            prod = st.number_input("Production (m³)", min_value=0.0, step=10.0)
            solar = st.selectbox("Solar Power Used?", ["Yes", "No"])
            diesel = st.number_input("Diesel Consumed (Liters)", min_value=0.0, step=1.0)
            
        submit = st.form_submit_button("Save Entry")
        if submit:
            new_row = {
                "Date": str(date_input),
                "Borehole": borehole,
                "Engine1_Hours": e1_hours,
                "Engine2_Hours": e2_hours,
                "Production_m3": prod,
                "Diesel_Liters": diesel
            }
            st.session_state.daily_data = pd.concat([st.session_state.daily_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Data for {borehole} saved successfully!")
            st.rerun()

    st.subheader("Stored Log Data")
    st.dataframe(st.session_state.daily_data, use_container_width=True)

# ==================== TAB 3: EXPORT REPORTS ====================
with tab3:
    st.header("Export Word Report (.docx)")
    st.write("Click the button below to generate and download the project report with current live data.")
    
    if st.button("Generate Word Report"):
        doc = Document()
        doc.add_heading('Water Supply & Borehole Management - Project Report', level=1)
        
        sections = [
            ("Stations", "Dhamuug Main, Afraag Main Station"),
            ("Modules", "Operations, Maintenance, Reports & Charts"),
            ("Dashboard Status", f"Total Records: {len(st.session_state.daily_data)} entries managed dynamically.")
        ]
        for title, text in sections:
            doc.add_heading(title, level=2)
            doc.add_paragraph(text)
            
        doc.add_heading("Current Web App Data Table", level=2)
        table = doc.add_table(rows=1, cols=4)
        
        # Fixed the cell indexing issue completely here:
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Date'
        hdr_cells[1].text = 'Borehole'
        hdr_cells[2].text = 'Production (m³)'
        hdr_cells[3].text = 'Diesel (L)'
        
        for index, row in st.session_state.daily_data.iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(row['Date'])
            row_cells[1].text = str(row['Borehole'])
            row_cells[2].text = str(row['Production_m3'])
            row_cells[3].text = str(row['Diesel_Liters'])

        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📥 Download Word File",
            data=bio.getvalue(),
            file_name="Borehole_Management_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
