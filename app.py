doc = Document()
        doc.add_heading("Water Supply & Borehole Management Report", level=1)

        doc.add_heading("Summary", level=2)
        doc.add_paragraph(
            f"Total Records: {len(st.session_state.daily_data)}"
        )

        doc.add_heading("System Modules", level=2)
        doc.add_paragraph("Operations, Maintenance, Monitoring, Reporting")

        # ================= TABLE =================
        doc.add_heading("Daily Data Table", level=2)

        table = doc.add_table(rows=1, cols=5)

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Date"
        hdr_cells[1].text = "Borehole"
        hdr_cells[2].text = "Production (m³)"
        hdr_cells[3].text = "Diesel (L)"
        hdr_cells[4].text = "Solar"

        for _, row in st.session_state.daily_data.iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(row["Date"])
            row_cells[1].text = str(row["Borehole"])
            row_cells[2].text = str(row["Production_m3"])
            row_cells[3].text = str(row["Diesel_Liters"])
            row_cells[4].text = str(row["Solar"])

        # ================= SAVE FILE =================
        bio = io.BytesIO()
        doc.save(bio)

        st.download_button(
            label="📥 Download Word Report",
            data=bio.getvalue(),
            file_name="Borehole_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
