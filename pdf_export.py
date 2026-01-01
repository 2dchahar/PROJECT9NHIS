from fpdf import FPDF

def export_pdf(query, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 8, f"Query:\n{query}\n\nSummary:\n{summary}")
    file_path = "summary.pdf"
    pdf.output(file_path)
    return file_path
