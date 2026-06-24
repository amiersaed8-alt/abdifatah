import streamlit as st, pandas as pd, plotly.express as px, io
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Borehole Management", layout="wide", page_icon="🚰")
st.title("🚰 Water Supply & Borehole Management Web App")

if "daily_data" not in st.session_state:
    st.session_state.daily_data = pd.DataFrame([
        {"Date": "2026-06-25", "Borehole": "Dhamuug Main Station", "Engine1_Hours": 8.0, "Engine2_Hours": 4.0, "Engine3_Hours": 0.0, "Production_m3": 120.0, "Diesel_Liters": 15.0}
    ])

t1, t2, t3 = st.tabs(["📊 Dashboard", "📝 Entry Form & Data", "📄 Export Reports"])

with t1:
    st.header("Borehole Performance & KPIs")
    df = st.session_state.daily_data
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Production (m³)", f"{df['Production_m3'].sum():,}")
    c2.metric("Total Diesel Used (L)", f"{df['Diesel_Liters'].sum():,}")
    c3.metric("Engine 1 Total Hours", f"{df['Engine1_Hours'].sum():,}")
    fig = px.bar(df, x="Date", y="Production_m3", color="Borehole", barmode="group", title="Daily Water Production")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.header("Daily Data Input Form")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("Date", datetime.now())
            bh = st.text_input("Qor Magaca Ceelka (Borehole Name)", "Dhamuug Main Station")
            e1 = st.number_input("Engine 1 Hours", min_value=0.0, step=0.5)
            e2 = st.number_input("Engine 2 Hours", min_value=0.0, step=0.5)
            e3 = st.number_input("Engine 3 Hours", min_value=0.0, step=0.5)
        with col2:
            pr = st.number_input("Production (m³)", min_value=0.0, step=10.0)
            ds = st.number_input("Diesel Consumed (Liters)", min_value=0.0, step=1.0)
        if st.form_submit_button("Save Entry"):
            new_row = {"Date": str(dt), "Borehole": bh, "Engine1_Hours": e1, "Engine2_Hours": e2, "Engine3_Hours": e3, "Production_m3": pr, "Diesel_Liters": ds}
            st.session_state.daily_data = pd.concat([st.session_state.daily_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Saved Successfully!"); st.rerun()
            
    st.subheader("Stored Log Data & Live Totals")
    df_display = st.session_state.daily_data.copy()
    totals = pd.DataFrame([{
        "Date": "TOTAL", "Borehole": "-", 
        "Engine1_Hours": df_display["Engine1_Hours"].sum(),
        "Engine2_Hours": df_display["Engine2_Hours"].sum(),
        "Engine3_Hours": df_display["Engine3_Hours"].sum(),
        "Production_m3": df_display["Production_m3"].sum(),
        "Diesel_Liters": df_display["Diesel_Liters"].sum()
    }])
    st.dataframe(pd.concat([df_display, totals], ignore_index=True), use_container_width=True)

with t3:
    st.header("Export Word Report")
    if st.button("Generate Word Report"):
        doc = Document()
        doc.add_heading('Water Supply Report', level=1)
        table = doc.add_table(rows=1, cols=6)
        for i, name in enumerate(['Date', 'Borehole', 'E1 Hours', 'E2 Hours', 'Prod (m³)', 'Diesel (L)']):
            table.rows.cells[i].text = name
        for _, r in st.session_state.daily_data.iterrows():
            cells = table.add_row().cells
            cells.text, cells.text, cells.text, cells.text, cells.text, cells.text = str(r['Date']), str(r['Borehole']), str(r['Engine1_Hours']), str(r['Engine2_Hours']), str(r['Production_m3']), str(r['Diesel_Liters'])
        bio = io.BytesIO(); doc.save(bio)
        st.download_button(label="📥 Download Word", data=bio.getvalue(), file_name="Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
