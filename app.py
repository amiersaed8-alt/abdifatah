import streamlit as st, pandas as pd, plotly.express as px, io
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Borehole Management", layout="wide", page_icon="🚰")
st.title("🚰 Water Supply & Borehole Management Web App")

if "daily_data" not in st.session_state:
    st.session_state.daily_data = pd.DataFrame([
        {"Date": "2026-06-20", "Borehole": "Dhamuug Main", "Engine1_Hours": 8.0, "Engine2_Hours": 4.0, "Production_m3": 120, "Diesel_Liters": 15},
        {"Date": "2026-06-21", "Borehole": "Afraag Main Station", "Engine1_Hours": 6.5, "Engine2_Hours": 5.0, "Production_m3": 95, "Diesel_Liters": 12}
    ])

t1, t2, t3 = st.tabs(["📊 Dashboard", "📝 Entry Form", "📄 Export Reports"])

with t1:
    st.header("Borehole Performance & KPIs")
    df = st.session_state.daily_data
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Production (m³)", f"{df['Production_m3'].sum():,}")
    c2.metric("Total Diesel Used (L)", f"{df['Diesel_Liters'].sum():,}")
    c3.metric("Engine 1 Hours", f"{df['Engine1_Hours'].sum():,}")
    fig = px.bar(df, x="Date", y="Production_m3", color="Borehole", barmode="group", title="Daily Water Production")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.header("Daily Data Input Form")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("Date", datetime.now())
            bh = st.selectbox("Select Borehole", ["Dhamuug Main", "Afraag Main Station"])
            e1 = st.number_input("Engine 1 Hours", min_value=0.0, step=0.5)
        with col2:
            pr = st.number_input("Production (m³)", min_value=0.0, step=10.0)
            ds = st.number_input("Diesel Consumed (Liters)", min_value=0.0, step=1.0)
        if st.form_submit_button("Save Entry"):
            new_row = {"Date": str(dt), "Borehole": bh, "Engine1_Hours": e1, "Engine2_Hours": 0.0, "Production_m3": pr, "Diesel_Liters": ds}
            st.session_state.daily_data = pd.concat([st.session_state.daily_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Saved!"); st.rerun()
    st.dataframe(st.session_state.daily_data, use_container_width=True)

with t3:
    st.header("Export Word Report")
    if st.button("Generate Word Report"):
        doc = Document()
        doc.add_heading('Water Supply Report', level=1)
        table = doc.add_table(rows=1, cols=4)
        for i, name in enumerate(['Date', 'Borehole', 'Prod (m³)', 'Diesel (L)']):
            table.rows[0].cells[i].text = name
        for _, r in st.session_state.daily_data.iterrows():
            cells = table.add_row().cells
            cells[0].text, cells[1].text, cells[2].text, cells[3].text = str(r['Date']), str(r['Borehole']), str(r['Production_m3']), str(r['Diesel_Liters'])
        bio = io.BytesIO(); doc.save(bio)
        st.download_button(label="📥 Download Word", data=bio.getvalue(), file_name="Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
