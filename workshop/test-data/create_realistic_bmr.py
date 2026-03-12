#!/usr/bin/env python3
"""Create a realistic-looking BMR (Batch Manufacturing Record) PDF for workshop testing.

This generates a form-style PDF that simulates a filled-in handwritten batch record
with realistic pharmaceutical data. Uses a handwriting-style font simulation via
italic Courier to approximate handwritten entries on a printed form template.
"""

from fpdf import FPDF


class BMRForm(FPDF):
    """Custom PDF class for BMR form generation."""

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(180, 0, 0)
        self.cell(0, 6, "SAMPLE - FOR WORKSHOP USE ONLY", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def form_label(self, text, w=50):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        self.cell(w, 8, text)

    def form_value(self, text, w=0):
        """Simulate handwritten entry using italic Courier."""
        self.set_font("Courier", "I", 11)
        self.set_text_color(0, 0, 140)
        self.cell(w, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def section_header(self, text):
        self.ln(3)
        self.set_fill_color(230, 230, 240)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  {text}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def draw_line(self):
        y = self.get_y()
        self.set_draw_color(180, 180, 180)
        self.line(15, y, 195, y)
        self.ln(2)


def create_bmr():
    pdf = BMRForm()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title block
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "BATCH MANUFACTURING RECORD", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "PharmaCorp Manufacturing Division  |  Form BMR-001 Rev 3.2", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Draw border around the form
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(12, 28, 186, 252)

    # --- Product Information Section ---
    pdf.section_header("SECTION A: PRODUCT INFORMATION")

    pdf.form_label("Product Name:")
    pdf.form_value("Amoxicillin 500mg Capsules")

    pdf.form_label("Batch Number:")
    pdf.form_value("BMR-2024-0847")

    pdf.form_label("Batch Size:")
    pdf.form_value("50,000 capsules (25.0 kg)")

    pdf.form_label("Manufacturing Date:")
    pdf.form_value("15-Mar-2024")

    pdf.draw_line()

    # --- Personnel Section ---
    pdf.section_header("SECTION B: PERSONNEL")

    pdf.form_label("Operator Initials:")
    pdf.form_value("JKL")

    pdf.form_label("Supervisor:")
    pdf.form_value("Dr. S. Patel")

    pdf.form_label("QA Reviewer:")
    pdf.form_value("M. Thompson")

    pdf.draw_line()

    # --- Equipment Section ---
    pdf.section_header("SECTION C: EQUIPMENT USED")

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(50, 7, "Equipment ID", border=1, fill=True)
    pdf.cell(70, 7, "Description", border=1, fill=True)
    pdf.cell(40, 7, "Calibration Due", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    rows = [
        ("MIX-401", "High-Shear Granulator", "2024-09-30"),
        ("GRAN-205", "Fluid Bed Dryer", "2024-08-15"),
        ("PRESS-112", "Rotary Tablet Press", "2024-11-01"),
    ]
    pdf.set_font("Courier", "I", 10)
    pdf.set_text_color(0, 0, 140)
    for eid, desc, cal in rows:
        pdf.cell(50, 7, eid, border=1)
        pdf.cell(70, 7, desc, border=1)
        pdf.cell(40, 7, cal, border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    pdf.draw_line()

    # --- Raw Materials / Ingredients Section ---
    pdf.section_header("SECTION D: RAW MATERIALS / INGREDIENTS")

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(55, 7, "Ingredient Name", border=1, fill=True)
    pdf.cell(25, 7, "Wt (kg)", border=1, fill=True)
    pdf.cell(40, 7, "Lot Number", border=1, fill=True)
    pdf.cell(35, 7, "Verified By", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    ingredients = [
        ("Amoxicillin Trihydrate", "25.00", "LOT-AM-20240115", "JKL"),
        ("Magnesium Stearate", "0.75", "LOT-MG-20240203", "JKL"),
        ("Microcrystalline Cellulose", "12.50", "LOT-MC-20240118", "JKL"),
    ]
    pdf.set_font("Courier", "I", 10)
    pdf.set_text_color(0, 0, 140)
    for name, wt, lot, ver in ingredients:
        pdf.cell(55, 7, name, border=1)
        pdf.cell(25, 7, wt, border=1)
        pdf.cell(40, 7, lot, border=1)
        pdf.cell(35, 7, ver, border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    pdf.draw_line()

    # --- Process Timing Section ---
    pdf.section_header("SECTION E: PROCESS TIMING")

    pdf.form_label("Start Time:")
    pdf.form_value("2024-03-15  06:30")

    pdf.form_label("End Time:")
    pdf.form_value("2024-03-15  14:45")

    pdf.form_label("Total Duration:")
    pdf.form_value("8 hours 15 minutes")

    # --- Footer ---
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "Form BMR-001 Rev 3.2  |  PharmaCorp Manufacturing  |  SAMPLE - FOR WORKSHOP USE ONLY", align="C")

    output_path = os.path.join(os.path.dirname(__file__), "bmr", "bmr-workshop-demo.pdf")
    pdf.output(output_path)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    import os
    create_bmr()
