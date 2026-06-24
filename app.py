]
        for title, text in sections:
            doc.add_heading(title, level=2)
            doc.add_paragraph(text)
            
        doc.add_heading("Current Web App Data Table", level=2)
        table = doc.add_table(rows=1, cols=4)
        
        hdr_cells = table.rows.cells
        hdr_cells.text = 'Date'
        hdr_cells.text = 'Borehole'
        hdr_cells.text = 'Production (m³)'
        hdr_cells.text = 'Diesel (L)'
        
        for index, row in st.session_state.daily_data.iterrows():
            row_cells = table.add_row().cells
            row_cells.text = str(row['Date'])
            row_cells.text = str(row['Borehole'])
            row_cells.text = str(row['Production_m3'])
            row_cells.text = str(row['Diesel_Liters'])

        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📥 Download Word File",
            data=bio.getvalue(),
            file_name="Borehole_Management_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
