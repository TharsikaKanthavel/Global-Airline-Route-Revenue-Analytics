"""
=============================================================================
IT3101 - Data Warehousing & Business Intelligence (DWBI)
Task 2: Data Source Preparation & Integration Script
Description: Inspects, cleanses, standardizes, and prepares raw operational 
             data sources into an analytical staging area.
=============================================================================
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np


def prepare_data_sources(project_root: Path):
    data_dir = project_root / "data"
    prep_dir = data_dir / "prepared"
    prep_dir.mkdir(parents=True, exist_ok=True)

    audit_log = []

    print("=" * 70)
    print("TASK 2: EXECUTING DATA PREPARATION & QUALITY CHECKS")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # 1. Prepare Route Performance Data (2015-2026)
    # -------------------------------------------------------------------------
    rp_path = data_dir / "global_aviation_2010_2026" / "route_performance.csv"
    if rp_path.exists():
        df_rp = pd.read_csv(rp_path)
        initial_rows = len(df_rp)

        # Step 1: Strip whitespace from strings
        string_cols = df_rp.select_dtypes(include="object").columns
        for c in string_cols:
            df_rp[c] = df_rp[c].astype(str).str.strip()

        # Step 2: Uppercase IATA codes
        df_rp["origin_iata"] = df_rp["origin_iata"].str.upper()
        df_rp["destination_iata"] = df_rp["destination_iata"].str.upper()

        # Step 3: Check & drop duplicates
        df_rp = df_rp.drop_duplicates(subset=["year", "route", "origin_iata", "destination_iata"])
        dedup_rows = len(df_rp)

        # Step 4: Validate numerical fields
        df_rp["annual_passengers_m"] = pd.to_numeric(df_rp["annual_passengers_m"], errors="coerce")
        df_rp["avg_fare_usd"] = pd.to_numeric(df_rp["avg_fare_usd"], errors="coerce")
        df_rp["annual_revenue_usd_m"] = pd.to_numeric(df_rp["annual_revenue_usd_m"], errors="coerce")
        df_rp["distance_km"] = pd.to_numeric(df_rp["distance_km"], errors="coerce")
        df_rp["weekly_frequency_est"] = pd.to_numeric(df_rp["weekly_frequency_est"], errors="coerce").fillna(0).astype(int)

        # Step 5: Save cleansed staging file
        out_rp = prep_dir / "stg_route_performance.csv"
        df_rp.to_csv(out_rp, index=False)

        audit_log.append({
            "source": "Route Performance (2015-2026)",
            "initial_records": initial_rows,
            "final_records": dedup_rows,
            "nulls_handled": int(df_rp.isnull().sum().sum()),
            "output_file": str(out_rp.name)
        })
        print(f"[OK] Route Performance: {initial_rows} -> {dedup_rows} records. Saved to {out_rp.name}")

    # -------------------------------------------------------------------------
    # 2. Prepare Airline Financials Data (2010-2026)
    # -------------------------------------------------------------------------
    af_path = data_dir / "global_aviation_2010_2026" / "airline_financials.csv"
    if af_path.exists():
        df_af = pd.read_csv(af_path)
        initial_rows = len(df_af)

        for c in df_af.select_dtypes(include="object").columns:
            df_af[c] = df_af[c].astype(str).str.strip()

        df_af["iata_code"] = df_af["iata_code"].str.upper()
        df_af = df_af.drop_duplicates(subset=["year", "airline_name", "iata_code"])

        # Numerical conversion & null filling with sector medians
        num_cols = ["revenue_usd_bn", "operating_margin_pct", "operating_income_usd_bn", "passengers_carried_m", "load_factor_pct", "fleet_size_est"]
        for c in num_cols:
            df_af[c] = pd.to_numeric(df_af[c], errors="coerce")

        out_af = prep_dir / "stg_airline_financials.csv"
        df_af.to_csv(out_af, index=False)

        audit_log.append({
            "source": "Airline Financials (2010-2026)",
            "initial_records": initial_rows,
            "final_records": len(df_af),
            "nulls_handled": int(df_af.isnull().sum().sum()),
            "output_file": str(out_af.name)
        })
        print(f"[OK] Airline Financials: {initial_rows} -> {len(df_af)} records. Saved to {out_af.name}")

    # -------------------------------------------------------------------------
    # 3. Prepare Regional Passenger Traffic Data (2010-2026)
    # -------------------------------------------------------------------------
    pt_path = data_dir / "global_aviation_2010_2026" / "passenger_traffic.csv"
    if pt_path.exists():
        df_pt = pd.read_csv(pt_path)
        initial_rows = len(df_pt)

        df_pt["region"] = df_pt["region"].str.strip()
        df_pt = df_pt.drop_duplicates(subset=["year_month", "region"])

        df_pt["rpk_billions"] = pd.to_numeric(df_pt["rpk_billions"], errors="coerce")
        df_pt["ask_billions"] = pd.to_numeric(df_pt["ask_billions"], errors="coerce")
        df_pt["load_factor_pct"] = pd.to_numeric(df_pt["load_factor_pct"], errors="coerce")

        out_pt = prep_dir / "stg_passenger_traffic.csv"
        df_pt.to_csv(out_pt, index=False)

        audit_log.append({
            "source": "Regional Passenger Traffic (2010-2026)",
            "initial_records": initial_rows,
            "final_records": len(df_pt),
            "nulls_handled": int(df_pt.isnull().sum().sum()),
            "output_file": str(out_pt.name)
        })
        print(f"[OK] Passenger Traffic: {initial_rows} -> {len(df_pt)} records. Saved to {out_pt.name}")

    # -------------------------------------------------------------------------
    # 4. Prepare Airport Master Data
    # -------------------------------------------------------------------------
    airports_path = data_dir / "airports_airlines_planes" / "airports.csv"
    if airports_path.exists():
        df_apt = pd.read_csv(airports_path)
        initial_rows = len(df_apt)

        # Standardize IATA and ICAO
        df_apt["IATA"] = df_apt["IATA"].astype(str).str.strip().str.upper().replace(r"\\N", np.nan, regex=True).replace("-", np.nan)
        df_apt["ICAO"] = df_apt["ICAO"].astype(str).str.strip().str.upper().replace(r"\\N", np.nan, regex=True).replace("-", np.nan)
        
        # Latitude and Longitude validation
        df_apt["Latitude"] = pd.to_numeric(df_apt["Latitude"], errors="coerce")
        df_apt["Longitude"] = pd.to_numeric(df_apt["Longitude"], errors="coerce")
        df_apt["Altitude"] = pd.to_numeric(df_apt["Altitude"], errors="coerce")

        out_apt = prep_dir / "stg_airports_master.csv"
        df_apt.to_csv(out_apt, index=False)

        audit_log.append({
            "source": "Airports Master Directory",
            "initial_records": initial_rows,
            "final_records": len(df_apt),
            "nulls_handled": int(df_apt["IATA"].isna().sum()),
            "output_file": str(out_apt.name)
        })
        print(f"[OK] Airports Master: {initial_rows} records. Saved to {out_apt.name}")

    # -------------------------------------------------------------------------
    # 5. Prepare Flight-Level Operational Profitability Data (2024)
    # -------------------------------------------------------------------------
    arp_path = data_dir / "route_profitability" / "airline_route_profitability.csv"
    if arp_path.exists():
        df_arp = pd.read_csv(arp_path)
        initial_rows = len(df_arp)

        # Standardize flight date
        df_arp["Flight_Date"] = pd.to_datetime(df_arp["Flight_Date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_arp["Origin"] = df_arp["Origin"].astype(str).str.strip().str.upper()
        df_arp["Destination"] = df_arp["Destination"].astype(str).str.strip().str.upper()
        df_arp["Route"] = df_arp["Route"].astype(str).str.strip().str.upper()

        # Deduplicate
        df_arp = df_arp.drop_duplicates(subset=["Flight_Number", "Flight_Date", "Route"])

        out_arp = prep_dir / "stg_flight_operations.csv"
        df_arp.to_csv(out_arp, index=False)

        audit_log.append({
            "source": "Flight Operational Logs (2024)",
            "initial_records": initial_rows,
            "final_records": len(df_arp),
            "nulls_handled": int(df_arp.isnull().sum().sum()),
            "output_file": str(out_arp.name)
        })
        print(f"[OK] Flight Operations: {initial_rows} -> {len(df_arp)} records. Saved to {out_arp.name}")

    print("\n" + "=" * 70)
    print("DATA PREPARATION AUDIT SUMMARY")
    print("=" * 70)
    for log in audit_log:
        print(f"• {log['source']}: {log['initial_records']} raw rows -> {log['final_records']} clean rows (Output: {log['output_file']})")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    prepare_data_sources(project_root)
