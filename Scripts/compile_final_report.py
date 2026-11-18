"""
compile_final_report.py
-----------------------
Compiles all 8 Task markdown files from the docs/ folder into a clean,
academic Microsoft Word (.docx) document formatted with:
- Standard Academic Font: Times New Roman (12pt for body, 1.5 line spacing).
- Proper heading hierarchy (Times New Roman, Bold, 16pt / 14pt / 12pt).
- NO raw source code blocks (omits raw DDL, SQL, Python scripts, focusing purely
  on academic explanations, architecture, dimensional designs, tables, and analytical findings).
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
OUTPUT_DOCX = os.path.join(os.path.dirname(__file__), "..", "SLIIT_IT3101_Final_DWBI_Report.docx")

TASK_FILES = [
    ("Task 1: Business Scenario & Dataset Selection", "Task_1_Business_Scenario_and_Dataset_Selection.md"),
    ("Task 2: Data Source Identification & Preparation", "Task_2_Data_Source_Identification_and_Preparation.md"),
    ("Task 3: Data Warehouse Architecture Design", "Task_3_Data_Warehouse_Architecture_Design.md"),
    ("Task 4: Dimensional Data Warehouse Design & Implementation", "Task_4_Dimensional_Data_Warehouse_Design_and_Implementation.md"),
    ("Task 5: ETL Process Development", "Task_5_ETL_Process_Development.md"),
    ("Task 6: Data Mart Development", "Task_6_Data_Mart_Development.md"),
    ("Task 7: OLAP Analysis & BI Dashboard Development", "Task_7_OLAP_Analysis_and_BI_Dashboard_Development.md"),
    ("Task 8: Business Insights & Strategic Recommendations", "Task_8_Business_Insights_and_Recommendations.md"),
]

FONT_NAME = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
DARK_GRAY = RGBColor(50, 50, 50)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_cover_page(doc):
    for _ in range(2):
        doc.add_paragraph()

    inst_p = doc.add_paragraph()
    inst_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    inst_run = inst_p.add_run("SRI LANKA INSTITUTE OF INFORMATION TECHNOLOGY\nFACULTY OF COMPUTING\nDEPARTMENT OF INFORMATION SYSTEMS")
    inst_run.font.name = FONT_NAME
    inst_run.font.size = Pt(14)
    inst_run.font.bold = True
    inst_run.font.color.rgb = BLACK

    for _ in range(2):
        doc.add_paragraph()

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("DESIGN AND IMPLEMENTATION OF A DATA WAREHOUSE AND BUSINESS INTELLIGENCE SOLUTION")
    title_run.font.name = FONT_NAME
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = BLACK

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("A Case Study in Global Commercial Airline Route Profitability & Operational Revenue Analytics (2010–2026)")
    sub_run.font.name = FONT_NAME
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = DARK_GRAY

    for _ in range(2):
        doc.add_paragraph()

    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    metadata = [
        ("Module Code & Title:", "IT3101 - Data Warehousing and Business Intelligence"),
        ("Assessment Component:", "Take-Home Assignment (End-to-End Project)"),
        ("Weighting / Maximum Marks:", "200 Marks (20% of Final Grade)"),
        ("Student Name:", "[ENTER YOUR FULL NAME HERE]"),
        ("Student Registration Number:", "[ENTER YOUR IT REGISTRATION NUMBER]"),
        ("Academic Year / Semester:", "3rd Year, 1st Semester - 2026"),
    ]

    col_widths = [Inches(2.8), Inches(3.7)]
    for i, (k, v) in enumerate(metadata):
        row = meta_table.rows[i]
        
        c0 = row.cells[0]
        c0.width = col_widths[0]
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(k)
        r0.font.name = FONT_NAME
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = BLACK
        set_cell_shading(c0, "F2F2F2")
        set_cell_margins(c0, 100, 100, 140, 140)

        c1 = row.cells[1]
        c1.width = col_widths[1]
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(v)
        r1.font.name = FONT_NAME
        r1.font.size = Pt(11)
        r1.font.color.rgb = BLACK
        if "[" in v:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(180, 0, 0)
        set_cell_shading(c1, "FFFFFF")
        set_cell_margins(c1, 100, 100, 140, 140)

    doc.add_page_break()

def parse_markdown_to_docx(doc, filepath):
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    table_lines = []
    in_code_block = False

    for line in lines:
        raw = line.rstrip()

        # OMIT CODE BLOCKS COMPLETELY (per user instructions: "you don't need to add codes")
        if raw.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            # Skip code content
            continue

        # Handle Markdown Tables
        if "|" in raw and not raw.startswith("#"):
            parts = [p.strip() for p in raw.split("|")[1:-1]]
            # Skip table divider row
            if all(re.match(r"^:?-+:?$", p) for p in parts if p):
                continue
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(parts)
            continue
        else:
            if in_table:
                # Flush table
                if len(table_lines) > 0:
                    num_cols = max(len(r) for r in table_lines)
                    tbl = doc.add_table(rows=len(table_lines), cols=num_cols)
                    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                    tbl.style = "Table Grid"
                    for r_idx, row_data in enumerate(table_lines):
                        for c_idx in range(num_cols):
                            cell_text = row_data[c_idx] if c_idx < len(row_data) else ""
                            cell = tbl.rows[r_idx].cells[c_idx]
                            p = cell.paragraphs[0]
                            p.paragraph_format.line_spacing = 1.15
                            p.paragraph_format.space_before = Pt(3)
                            p.paragraph_format.space_after = Pt(3)
                            run = p.add_run(cell_text)
                            run.font.name = FONT_NAME
                            run.font.size = Pt(10)
                            set_cell_margins(cell, 80, 80, 100, 100)
                            if r_idx == 0:
                                set_cell_shading(cell, "E0E0E0")
                                run.font.bold = True
                                run.font.color.rgb = BLACK
                            else:
                                if r_idx % 2 == 1:
                                    set_cell_shading(cell, "F9F9F9")
                                else:
                                    set_cell_shading(cell, "FFFFFF")
                                run.font.color.rgb = BLACK
                in_table = False
                table_lines = []

        # Empty lines
        if not raw.strip():
            continue

        # Headings
        if raw.startswith("# "):
            h_text = raw[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = FONT_NAME
            r.font.size = Pt(16)
            r.font.bold = True
            r.font.color.rgb = BLACK
        elif raw.startswith("## "):
            h_text = raw[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = FONT_NAME
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = BLACK
        elif raw.startswith("### "):
            h_text = raw[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = FONT_NAME
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = BLACK
        elif raw.startswith("#### "):
            h_text = raw[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = FONT_NAME
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.italic = True
            r.font.color.rgb = BLACK
        # Bullet list
        elif raw.startswith("- ") or raw.startswith("* ") or re.match(r"^\d+\.\s", raw):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            content = re.sub(r"^[-*]\s+|\d+\.\s+", "", raw)
            parts = re.split(r"(\*\*.*?\*\*)", content)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                else:
                    r = p.add_run(part)
                r.font.name = FONT_NAME
                r.font.size = Pt(11)
                r.font.color.rgb = BLACK
        else:
            # Standard academic body paragraph (Times New Roman, 12pt, 1.15 line spacing)
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            parts = re.split(r"(\*\*.*?\*\*)", raw)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                else:
                    r = p.add_run(part)
                r.font.name = FONT_NAME
                r.font.size = Pt(11.5)
                r.font.color.rgb = BLACK

    # Flush dangling table
    if in_table and len(table_lines) > 0:
        num_cols = max(len(r) for r in table_lines)
        tbl = doc.add_table(rows=len(table_lines), cols=num_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.style = "Table Grid"
        for r_idx, row_data in enumerate(table_lines):
            for c_idx in range(num_cols):
                cell_text = row_data[c_idx] if c_idx < len(row_data) else ""
                cell = tbl.rows[r_idx].cells[c_idx]
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                run = p.add_run(cell_text)
                run.font.name = FONT_NAME
                run.font.size = Pt(10)
                set_cell_margins(cell, 80, 80, 100, 100)
                if r_idx == 0:
                    set_cell_shading(cell, "E0E0E0")
                    run.font.bold = True
                    run.font.color.rgb = BLACK
                else:
                    if r_idx % 2 == 1:
                        set_cell_shading(cell, "F9F9F9")
                    else:
                        set_cell_shading(cell, "FFFFFF")
                    run.font.color.rgb = BLACK

def compile_academic_report():
    print("Compiling Academic Final Report in Times New Roman (No code blocks)...")
    doc = docx.Document()

    # Standard academic 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Cover Page
    add_cover_page(doc)

    # 2. Table of Contents
    toc_p = doc.add_paragraph()
    toc_run = toc_p.add_run("TABLE OF CONTENTS")
    toc_run.font.name = FONT_NAME
    toc_run.font.size = Pt(14)
    toc_run.font.bold = True
    toc_run.font.color.rgb = BLACK

    contents = [
        "1. Task 1: Business Scenario and Dataset Selection (10 Marks)",
        "2. Task 2: Data Source Identification and Preparation (10 Marks)",
        "3. Task 3: Data Warehouse Architecture Design (10 Marks)",
        "4. Task 4: Dimensional Data Warehouse Design and Implementation (20 Marks)",
        "5. Task 5: ETL Process Development (20 Marks)",
        "6. Task 6: Data Mart Development (10 Marks)",
        "7. Task 7: OLAP Analysis and Business Intelligence Dashboard Development (15 Marks)",
        "8. Task 8: Business Insights and Strategic Recommendations (5 Marks)",
        "9. Executive Summary of 20 Analytical Business Discoveries"
    ]
    for c in contents:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(c)
        r.font.name = FONT_NAME
        r.font.size = Pt(11)
        r.font.color.rgb = BLACK

    doc.add_page_break()

    # 3. Tasks 1 to 8
    for title, fname in TASK_FILES:
        print(f"Adding {title}...")
        fpath = os.path.join(DOCS_DIR, fname)
        parse_markdown_to_docx(doc, fpath)
        doc.add_page_break()

    # 4. Summary of Insights
    appendix_path = os.path.join(DOCS_DIR, "Comprehensive_Business_Insights_Summary.md")
    if os.path.exists(appendix_path):
        print("Adding Insights Summary...")
        parse_markdown_to_docx(doc, appendix_path)

    doc.save(OUTPUT_DOCX)
    print(f"SUCCESS: Academic report saved to {OUTPUT_DOCX}")

if __name__ == "__main__":
    compile_academic_report()
