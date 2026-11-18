"""
=============================================================================
IT3101 - Data Warehousing & Business Intelligence (DWBI)
Project: Global Airline Route & Revenue Analytics Solution (2010-2026)
Script: inspect_and_catalog_datasets.py
Description: Generates an automated, comprehensive catalog and audit report
             of all acquired datasets, including column counts, row counts,
             data types, and temporal ranges (2010-2026).
=============================================================================
"""

import json
import os
from pathlib import Path
import pandas as pd


def generate_dataset_catalog(project_dir: Path) -> None:
    data_dir = project_dir / "data"
    output_md = project_dir / "scripts" / "DATASET_CATALOG.md"
    output_json = project_dir / "scripts" / "dataset_metadata.json"

    catalog = []

    print("Scanning datasets in:", data_dir)

    for root, _, files in os.walk(data_dir):
        for f in sorted(files):
            if f.endswith(".csv"):
                file_path = Path(root) / f
                rel_path = file_path.relative_to(project_dir)
                file_size_kb = round(os.path.getsize(file_path) / 1024, 2)

                try:
                    df = pd.read_csv(file_path, low_memory=False)
                    num_rows, num_cols = df.shape

                    # Detect time range
                    time_info = "N/A"
                    for col in df.columns:
                        col_lower = col.lower()
                        if "year" in col_lower and not "month" in col_lower:
                            unique_years = sorted([int(y) for y in df[col].dropna().unique() if str(y).replace(".0","").isdigit()])
                            if unique_years:
                                time_info = f"{min(unique_years)} - {max(unique_years)}"
                            break
                        elif "date" in col_lower:
                            dates = df[col].dropna().astype(str)
                            time_info = f"{dates.min()} to {dates.max()}"
                            break

                    col_summary = []
                    for c in df.columns:
                        col_summary.append({
                            "name": c,
                            "dtype": str(df[c].dtype),
                            "null_count": int(df[c].isnull().sum()),
                            "sample": str(df[c].dropna().iloc[0]) if not df[c].dropna().empty else None
                        })

                    catalog.append({
                        "file_name": f,
                        "relative_path": str(rel_path).replace("\\", "/"),
                        "size_kb": file_size_kb,
                        "rows": num_rows,
                        "columns_count": num_cols,
                        "temporal_coverage": time_info,
                        "columns": col_summary
                    })
                    print(f"[AUDITED] {f}: {num_rows} rows, {num_cols} cols, Coverage: {time_info}")
                except Exception as e:
                    print(f"[ERROR] Failed to audit {f}: {e}")

    # Save to JSON
    with open(output_json, "w", encoding="utf-8") as jf:
        json.dump(catalog, jf, indent=2)

    # Save to Markdown
    with open(output_md, "w", encoding="utf-8") as mf:
        mf.write("# Global Airline Route & Revenue Analytics (2010–2026)\n")
        mf.write("## Technical Dataset Catalog & Audit Report\n\n")
        mf.write(f"**Generated on:** 2026-09-26  \n")
        mf.write(f"**Total CSV Data Files Audited:** {len(catalog)}  \n\n")

        mf.write("### 1. High-Level Summary Table\n\n")
        mf.write("| File Name | Path | Rows | Columns | Size (KB) | Temporal Coverage |\n")
        mf.write("| :--- | :--- | :---: | :---: | :---: | :---: |\n")
        for item in catalog:
            mf.write(f"| `{item['file_name']}` | `{item['relative_path']}` | {item['rows']:,} | {item['columns_count']} | {item['size_kb']} KB | {item['temporal_coverage']} |\n")

        mf.write("\n\n### 2. Detailed Attribute Breakdown\n\n")
        for item in catalog:
            mf.write(f"#### `{item['file_name']}`\n")
            mf.write(f"- **Path:** `{item['relative_path']}`\n")
            mf.write(f"- **Record Count:** {item['rows']:,} rows\n")
            mf.write(f"- **Column Count:** {item['columns_count']} columns\n")
            mf.write(f"- **Coverage:** {item['temporal_coverage']}\n\n")
            mf.write("| Attribute Name | Data Type | Null Count | Sample Value |\n")
            mf.write("| :--- | :--- | :---: | :--- |\n")
            for col in item["columns"][:15]:  # top 15 columns for readability
                mf.write(f"| `{col['name']}` | `{col['dtype']}` | {col['null_count']} | {col['sample']} |\n")
            if len(item["columns"]) > 15:
                mf.write(f"| *... and {len(item['columns']) - 15} more attributes* | | | |\n")
            mf.write("\n---\n\n")

    print(f"\n[SUCCESS] Markdown Catalog generated at: {output_md}")
    print(f"[SUCCESS] JSON Metadata saved at: {output_json}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    generate_dataset_catalog(project_root)
