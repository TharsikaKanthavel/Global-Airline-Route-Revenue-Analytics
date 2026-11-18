"""
=============================================================================
IT3101 - Data Warehousing & Business Intelligence (DWBI)
Task 6: Build Departmental Data Mart Script
Description: Applies SQL views and analytical cubes to airline_dw.db and
             exports specialized Data Mart tables to CSV for BI tools.
=============================================================================
"""

import sqlite3
from pathlib import Path
import pandas as pd


def build_data_mart(project_root: Path):
    db_path = project_root / "data" / "warehouse" / "airline_dw.db"
    sql_path = project_root / "sql" / "data_mart_views.sql"
    out_dir = project_root / "data" / "warehouse"

    print("=" * 70)
    print("TASK 6: BUILDING ROUTE PROFITABILITY & REVENUE DATA MART")
    print(f"Target Database: {db_path}")
    print("=" * 70)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute SQL Views
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Execute script statements
    cursor.executescript(sql_script)
    conn.commit()
    print("[OK] Data Mart SQL Views created successfully in database.")

    # Export views to CSV for Power BI / Tableau direct access
    views = [
        "DM_Route_Profitability_Summary",
        "DM_Regional_Corridor_Performance",
        "DM_Underperforming_Routes_Watchlist",
        "DM_Aircraft_Fleet_Efficiency"
    ]

    for v in views:
        df = pd.read_sql_query(f"SELECT * FROM {v}", conn)
        out_csv = out_dir / f"{v}.csv"
        df.to_csv(out_csv, index=False)
        print(f"  • Exported '{v}': {len(df):,} rows -> {out_csv.name}")

    conn.close()
    print("\n" + "=" * 70)
    print("[SUCCESS] Route Profitability & Revenue Data Mart is Active & Ready.")
    print("=" * 70)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    build_data_mart(root)
