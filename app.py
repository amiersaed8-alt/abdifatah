fig_bh = px.bar(df, x="Borehole", y="Production_m3", color="Station", title="Production by Borehole & Station")
        st.plotly_chart(fig_bh, use_container_width=True)
    with c2:
        st.write("Engine vs Solar Hours")
        df_melted = df.melt(id_vars=["Borehole"], value_vars=["Engine_Hours", "Solar_Hours"], var_name="Type", value_name="Hours")
        fig_eng = px.bar(df_melted, x="Borehole", y="Hours", color="Type", barmode="group", title="Engine vs Solar Hours")
        st.plotly_chart(fig_eng, use_container_width=True)

    st.markdown("---")

    # --- 4. MAINTENANCE ---
    st.subheader("🔧 Maintenance (Dayactirka)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Engine Maintenance Cost", f"${df['E_Maint'].sum():,}")
    m2.metric("Borehole/Pump Cost", f"${df['B_Maint'].sum():,}")
    m3.metric("Solar Maintenance Cost", f"${df['S_Maint'].sum():,}")
    
    total_m_cost = df_month['E_Maint'].sum() + df_month['B_Maint'].sum() + df_month['S_Maint'].sum()
    m4.metric("Monthly Maint Cost (Total)", f"${total_m_cost:,}", delta_color="inverse")

# ==================== TAB 2: ENTRY FORM ====================
with t2:
    st.header("📝 Foomka Gelinta Xogta Maalinlahay")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("Date", datetime.now())
            stn = st.selectbox("Select Station", ["Dhamuug", "Afraag"])
            bh = st.text_input("Qor Magaca Ceelka (Borehole)", "Dhamuug-01")
            e1 = st.number_input("Engine Hours", min_value=0.0, step=0.5)
            sl = st.number_input("Solar Hours", min_value=0.0, step=0.5)
        with col2:
            pr = st.number_input("Production (m³)", min_value=0.0, step=10.0)
            ds = st.number_input("Diesel Consumed (Liters)", min_value=0.0, step=1.0)
            em = st.number_input("Engine Maint Cost ($)", min_value=0.0, step=5.0)
            bm = st.number_input("Borehole/Pump Maint Cost ($)", min_value=0.0, step=5.0)
            sm = st.number_input("Solar Maint Cost ($)", min_value=0.0, step=5.0)
            
        if st.form_submit_button("Save Entry"):
            new_row = {"Date": pd.to_datetime(dt), "Station": stn, "Borehole": bh, "Engine_Hours": e1, "Solar_Hours": sl, "Production_m3": pr, "Diesel_Liters": ds, "E_Maint": em, "B_Maint": bm, "S_Maint": sm}
            st.session_state.daily_data = pd.concat([st.session_state.daily_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Xogtii waa la kaydiyey!"); st.rerun()
            
    st.subheader("Shaxda Xogta Guud")
    st.dataframe(st.session_state.daily_data, use_container_width=True)

# ==================== TAB 3: EXPORT ====================
with t3:
    st.header("📄 Export Word Report")
    if st.button("Generate Word Report"):
        doc = Document()
        doc.add_heading('Water Supply Executive Report', level=1)
        table = doc.add_table(rows=1, cols=6)
        for i, name in enumerate(['Date', 'Borehole', 'Prod (m³)', 'Diesel (L)', 'Eng Hours', 'Maint Cost']):
            table.rows.cells[i].text = name
        for _, r in st.session_state.daily_data.iterrows():
            cells = table.add_row().cells
            cells.text, cells.text, cells.text, cells.text, cells.text, cells.text = str(r['Date'])[:10], str(r['Borehole']), str(r['Production_m3']), str(r['Diesel_Liters']), str(r['Engine_Hours']), f"${r['E_Maint']+r['B_Maint']+r['S_Maint']}"
        bio = io.BytesIO(); doc.save(bio)
        st.download_button(label="📥 Download Word", data=bio.getvalue(), file_name="Executive_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
