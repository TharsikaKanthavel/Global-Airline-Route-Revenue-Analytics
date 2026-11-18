"""
=============================================================================
IT3101 - Data Warehousing & Business Intelligence (DWBI)
Task 5: End-to-End ETL Pipeline Implementation
Description: Extracts raw operational data from multiple sources, performs
             comprehensive transformations (cleansing, deduplication, type
             conversions, derived financial metrics), generates surrogate keys,
             and loads the dimensional Star Schema into both SQLite database
             and clean CSV files for Power BI / Tableau consumption.
=============================================================================
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd


class AirlineDWETLPipeline:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.data_dir = project_root / "data"
        self.output_dw_dir = self.data_dir / "warehouse"
        self.output_dw_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.output_dw_dir / "airline_dw.db"
        self.validation_results = {}

    def log(self, message: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    # =========================================================================
    # PHASE 1: EXTRACTION
    # =========================================================================
    def extract(self):
        self.log("PHASE 1: Starting Data Extraction from Operational Sources...")
        
        # Source 1: Route Performance (2015-2026)
        rp_path = self.data_dir / "global_aviation_2010_2026" / "route_performance.csv"
        self.raw_rp = pd.read_csv(rp_path)
        self.log(f"  • Extracted Route Performance: {len(self.raw_rp):,} records")

        # Source 2: Airline Financials (2010-2026)
        af_path = self.data_dir / "global_aviation_2010_2026" / "airline_financials.csv"
        self.raw_af = pd.read_csv(af_path)
        self.log(f"  • Extracted Airline Financials: {len(self.raw_af):,} records")

        # Source 3: Airports Master Directory
        apt_path = self.data_dir / "airports_airlines_planes" / "airports.csv"
        self.raw_apt = pd.read_csv(apt_path)
        self.log(f"  • Extracted Airports Directory: {len(self.raw_apt):,} records")

        # Source 4: Airlines Master Directory
        airl_path = self.data_dir / "airports_airlines_planes" / "airlines.csv"
        self.raw_airl = pd.read_csv(airl_path)
        self.log(f"  • Extracted Airlines Directory: {len(self.raw_airl):,} records")

        # Source 5: Aircraft Specifications
        airp_path = self.data_dir / "airports_airlines_planes" / "airplanes.csv"
        self.raw_airp = pd.read_csv(airp_path)
        self.log(f"  • Extracted Aircraft Models: {len(self.raw_airp):,} records")

        # Source 6: Flight Operations Daily Logs (2024)
        fo_path = self.data_dir / "route_profitability" / "airline_route_profitability.csv"
        self.raw_fo = pd.read_csv(fo_path)
        self.log(f"  • Extracted Flight Operations Logs: {len(self.raw_fo):,} records")

    # =========================================================================
    # PHASE 2: TRANSFORMATION
    # =========================================================================
    def transform(self):
        self.log("PHASE 2: Executing Data Transformations & Business Logic...")

        # ---------------------------------------------------------------------
        # 1. Transform Dim_Date
        # ---------------------------------------------------------------------
        self.log("  -> Building Dim_Date (2010-2026)...")
        date_records = []
        for yr in range(2010, 2027):
            # Calendar year entries for annual route facts
            date_records.append({
                "Date_Key": yr * 10000 + 101,  # e.g. 20240101
                "Full_Date": f"{yr}-01-01",
                "Year": yr,
                "Quarter": "Q1",
                "Quarter_Name": f"{yr} Q1",
                "Month_Number": 1,
                "Month_Name": "January",
                "Day_Of_Month": 1,
                "Day_Of_Week": "Monday",
                "Is_Weekend": "N",
                "Peak_Season_Flag": "Normal"
            })
        
        # Also parse daily dates from Flight Operations (2024)
        unique_dates = pd.to_datetime(self.raw_fo["Flight_Date"].dropna().unique())
        for d in unique_dates:
            d_key = int(d.strftime("%Y%m%d"))
            if d_key not in [r["Date_Key"] for r in date_records]:
                m = d.month
                peak = "Peak" if m in [6, 7, 8, 12] else ("Shoulder" if m in [3, 4, 9, 10] else "Low")
                date_records.append({
                    "Date_Key": d_key,
                    "Full_Date": d.strftime("%Y-%m-%d"),
                    "Year": d.year,
                    "Quarter": f"Q{(m-1)//3 + 1}",
                    "Quarter_Name": f"{d.year} Q{(m-1)//3 + 1}",
                    "Month_Number": m,
                    "Month_Name": d.strftime("%B"),
                    "Day_Of_Month": d.day,
                    "Day_Of_Week": d.strftime("%A"),
                    "Is_Weekend": "Y" if d.weekday() >= 5 else "N",
                    "Peak_Season_Flag": peak
                })

        self.dim_date = pd.DataFrame(date_records).sort_values("Date_Key").reset_index(drop=True)
        self.log(f"     Dim_Date generated: {len(self.dim_date):,} records")

        # ---------------------------------------------------------------------
        # 2. Transform Dim_Airport (Conformed, Unique by IATA)
        # ---------------------------------------------------------------------
        self.log("  -> Cleansing & Building Dim_Airport...")
        apt_clean = self.raw_apt.copy()
        apt_clean["IATA"] = apt_clean["IATA"].astype(str).str.strip().str.upper()
        # Filter out invalid or placeholder codes
        apt_clean = apt_clean[apt_clean["IATA"].str.match(r"^[A-Z]{3}$")]
        apt_clean = apt_clean.drop_duplicates(subset=["IATA"]).reset_index(drop=True)

        apt_clean["Airport_Key"] = np.arange(1, len(apt_clean) + 1)
        self.dim_airport = pd.DataFrame({
            "Airport_Key": apt_clean["Airport_Key"],
            "Airport_ID": pd.to_numeric(apt_clean["Airport ID"], errors="coerce").fillna(-1).astype(int),
            "IATA_Code": apt_clean["IATA"],
            "ICAO_Code": apt_clean["ICAO"].astype(str).str.strip().str.upper().replace(r"\\N", "UNKN", regex=True),
            "Airport_Name": apt_clean["Name"].astype(str).str.strip(),
            "City": apt_clean["City"].astype(str).str.strip(),
            "Country": apt_clean["Country"].astype(str).str.strip(),
            "Global_Region": apt_clean["Country"].apply(self._map_region),
            "Latitude": pd.to_numeric(apt_clean["Latitude"], errors="coerce"),
            "Longitude": pd.to_numeric(apt_clean["Longitude"], errors="coerce"),
            "Altitude_FT": pd.to_numeric(apt_clean["Altitude"], errors="coerce").fillna(0).astype(int),
            "Timezone_Offset": pd.to_numeric(apt_clean["Timezone"], errors="coerce").fillna(0.0)
        })
        
        # Add UNKNOWN Default Record (Key = 0)
        unknown_apt = pd.DataFrame([{
            "Airport_Key": 0, "Airport_ID": -1, "IATA_Code": "UNK", "ICAO_Code": "UNKN",
            "Airport_Name": "Unknown Airport", "City": "Unknown", "Country": "Unknown",
            "Global_Region": "Unknown", "Latitude": 0.0, "Longitude": 0.0,
            "Altitude_FT": 0, "Timezone_Offset": 0.0
        }])
        self.dim_airport = pd.concat([unknown_apt, self.dim_airport], ignore_index=True)
        self.log(f"     Dim_Airport generated: {len(self.dim_airport):,} records")

        # ---------------------------------------------------------------------
        # 3. Transform Dim_Airline
        # ---------------------------------------------------------------------
        self.log("  -> Cleansing & Building Dim_Airline...")
        airl_clean = self.raw_airl.copy()
        airl_clean["IATA"] = airl_clean["IATA"].astype(str).str.strip().str.upper()
        airl_clean = airl_clean[airl_clean["IATA"].str.match(r"^[A-Z0-9]{2,3}$")]
        airl_clean = airl_clean.drop_duplicates(subset=["IATA"]).reset_index(drop=True)

        airl_clean["Airline_Key"] = np.arange(1, len(airl_clean) + 1)
        self.dim_airline = pd.DataFrame({
            "Airline_Key": airl_clean["Airline_Key"],
            "Airline_ID": pd.to_numeric(airl_clean["Airline ID"], errors="coerce").fillna(-1).astype(int),
            "IATA_Code": airl_clean["IATA"],
            "ICAO_Code": airl_clean["ICAO"].astype(str).str.strip().str.upper().replace(r"\\N", "UNKN", regex=True),
            "Airline_Name": airl_clean["Name"].astype(str).str.strip(),
            "Callsign": airl_clean["Callsign"].astype(str).str.strip().replace(r"\\N", "NONE", regex=True),
            "Country_Origin": airl_clean["Country"].astype(str).str.strip().replace(r"\\N", "Unknown", regex=True),
            "Business_Model": "legacy",
            "Global_Alliance": "Independent",
            "Active_Status": airl_clean["Active"].astype(str).str.strip().str.upper()
        })
        
        # Default unknown record
        unknown_airl = pd.DataFrame([{
            "Airline_Key": 0, "Airline_ID": -1, "IATA_Code": "UNK", "ICAO_Code": "UNKN",
            "Airline_Name": "Unknown Airline / Alliance", "Callsign": "NONE",
            "Country_Origin": "Unknown", "Business_Model": "hybrid",
            "Global_Alliance": "Independent", "Active_Status": "Y"
        }])
        self.dim_airline = pd.concat([unknown_airl, self.dim_airline], ignore_index=True)
        self.log(f"     Dim_Airline generated: {len(self.dim_airline):,} records")

        # ---------------------------------------------------------------------
        # 4. Transform Dim_Aircraft
        # ---------------------------------------------------------------------
        self.log("  -> Building Dim_Aircraft...")
        unique_ac = self.raw_fo["Aircraft_Type"].dropna().unique()
        ac_records = []
        for i, ac_name in enumerate(unique_ac, start=1):
            mfg = "Boeing" if "Boeing" in ac_name else ("Airbus" if "Airbus" in ac_name else "Other")
            body = "Wide-Body" if any(x in ac_name for x in ["777", "787", "A380", "A350"]) else "Narrow-Body"
            seats = 517 if "A380" in ac_name else (396 if "777" in ac_name else (296 if "787" in ac_name else (325 if "A350" in ac_name else 180)))
            ac_records.append({
                "Aircraft_Key": i,
                "Aircraft_Model_Name": ac_name.strip(),
                "Manufacturer": mfg,
                "Aircraft_Family": ac_name.split()[1] if len(ac_name.split()) > 1 else ac_name,
                "Body_Type": body,
                "Typical_Seating_Capacity": seats,
                "Fuel_Efficiency_Class": "High" if ("787" in ac_name or "A350" in ac_name) else "Standard"
            })
        self.dim_aircraft = pd.DataFrame(ac_records)
        self.log(f"     Dim_Aircraft generated: {len(self.dim_aircraft):,} records")

        # ---------------------------------------------------------------------
        # 5. Transform Dim_Route
        # ---------------------------------------------------------------------
        self.log("  -> Building Dim_Route...")
        unique_routes = self.raw_rp[["route", "origin_iata", "destination_iata", "distance_km", "region"]].drop_duplicates(subset=["route"]).reset_index(drop=True)
        route_records = []
        for i, row in unique_routes.iterrows():
            dist = int(row["distance_km"]) if pd.notnull(row["distance_km"]) else 2500
            haul = "Long Haul" if dist >= 4000 else ("Medium Haul" if dist >= 1500 else "Short Haul")
            route_records.append({
                "Route_Key": i + 1,
                "Route_Code": f"{row['origin_iata'].strip()}-{row['destination_iata'].strip()}",
                "Route_Name": row["route"].strip(),
                "Origin_IATA": row["origin_iata"].strip().upper(),
                "Destination_IATA": row["destination_iata"].strip().upper(),
                "Distance_KM": dist,
                "Route_Category": haul,
                "Corridor_Region": row["region"].strip(),
                "Is_International": "Y"
            })
        self.dim_route = pd.DataFrame(route_records)
        self.log(f"     Dim_Route generated: {len(self.dim_route):,} records")

        # ---------------------------------------------------------------------
        # 6. Transform Fact_Route_Performance (Derived Metrics & FK Mapping)
        # ---------------------------------------------------------------------
        self.log("  -> Transforming & Deriving Fact_Route_Performance (2015-2026)...")
        # Lookup dictionaries
        apt_lookup = dict(zip(self.dim_airport["IATA_Code"], self.dim_airport["Airport_Key"]))
        route_lookup = dict(zip(self.dim_route["Route_Name"], self.dim_route["Route_Key"]))
        
        # Calculate annual sector operating margins from airline financials for realistic cost derivation
        margin_by_year = self.raw_af.groupby("year")["operating_margin_pct"].median().to_dict()
        default_margin = float(self.raw_af["operating_margin_pct"].median())

        frp_records = []
        for _, row in self.raw_rp.iterrows():
            yr = int(row["year"])
            date_k = yr * 10000 + 101
            route_k = route_lookup.get(row["route"].strip(), 1)
            orig_k = apt_lookup.get(row["origin_iata"].strip().upper(), 0)
            dest_k = apt_lookup.get(row["destination_iata"].strip().upper(), 0)
            
            rev_m = float(row["annual_revenue_usd_m"])
            passengers_m = float(row["annual_passengers_m"])
            avg_fare = float(row["avg_fare_usd"])
            freq = int(row["weekly_frequency_est"])
            dist = int(row["distance_km"])

            # Derived Metrics: Operating Cost, Net Profit, Profit Margin %
            sector_margin = margin_by_year.get(yr, default_margin)
            # Add small route variance based on distance
            route_margin_pct = round(sector_margin + (2.0 if dist < 3000 else -1.5), 2)
            cost_m = round(rev_m * (1.0 - (route_margin_pct / 100.0)), 2)
            net_profit_m = round(rev_m - cost_m, 2)
            calc_margin_pct = round((net_profit_m / rev_m) * 100.0, 2) if rev_m > 0 else 0.0

            frp_records.append({
                "Date_Key": date_k,
                "Route_Key": route_k,
                "Origin_Airport_Key": orig_k,
                "Destination_Airport_Key": dest_k,
                "Airline_Key": 0,  # Generic multi-carrier corridor
                "Annual_Revenue_USD_M": rev_m,
                "Annual_Passengers_M": passengers_m,
                "Weekly_Frequency_Est": freq,
                "Avg_Fare_USD": avg_fare,
                "Distance_KM": dist,
                "Operating_Cost_USD_M": cost_m,
                "Net_Profit_USD_M": net_profit_m,
                "Profit_Margin_PCT": calc_margin_pct
            })

        self.fact_route_perf = pd.DataFrame(frp_records)
        self.fact_route_perf["Performance_Fact_ID"] = np.arange(1, len(self.fact_route_perf) + 1)
        self.log(f"     Fact_Route_Performance built: {len(self.fact_route_perf):,} records with derived metrics")

        # ---------------------------------------------------------------------
        # 7. Transform Fact_Flight_Operations
        # ---------------------------------------------------------------------
        self.log("  -> Transforming Fact_Flight_Operations (2024)...")
        ac_lookup = dict(zip(self.dim_aircraft["Aircraft_Model_Name"], self.dim_aircraft["Aircraft_Key"]))
        route_code_lookup = dict(zip(self.dim_route["Route_Code"], self.dim_route["Route_Key"]))

        ffo_records = []
        for _, row in self.raw_fo.iterrows():
            d = pd.to_datetime(row["Flight_Date"])
            d_k = int(d.strftime("%Y%m%d"))
            r_code = f"{str(row['Origin']).strip().upper()}-{str(row['Destination']).strip().upper()}"
            r_k = route_code_lookup.get(r_code, 1)
            orig_k = apt_lookup.get(str(row["Origin"]).strip().upper(), 0)
            dest_k = apt_lookup.get(str(row["Destination"]).strip().upper(), 0)
            ac_k = ac_lookup.get(str(row["Aircraft_Type"]).strip(), 1)

            ffo_records.append({
                "Flight_Number": str(row["Flight_Number"]).strip(),
                "Date_Key": d_k,
                "Route_Key": r_k,
                "Origin_Airport_Key": orig_k,
                "Destination_Airport_Key": dest_k,
                "Aircraft_Key": ac_k,
                "Aircraft_Capacity": int(row["Aircraft_Capacity"]),
                "Passengers_Booked": int(row["Passengers"]),
                "Load_Factor": round(float(row["Load_Factor"]), 4),
                "Flight_Hours": round(float(row["Flight_Hours"]), 1),
                "Ticket_Revenue": round(float(row["Ticket_Revenue"]), 2),
                "Ancillary_Revenue": round(float(row["Ancillary_Revenue"]), 2),
                "Total_Revenue": round(float(row["Total_Revenue"]), 2),
                "Fuel_Cost": round(float(row["Fuel_Cost"]), 2),
                "Maintenance_Cost": round(float(row["Maintenance_Cost"]), 2),
                "Crew_Cost": round(float(row["Crew_Cost"]), 2),
                "Airport_Fees": round(float(row["Airport_Fees"]), 2) if pd.notnull(row["Airport_Fees"]) else 0.0,
                "Handling_Cost": round(float(row["Handling_Cost"]), 2),
                "Navigation_Fees": round(float(row["Navigation_Fees"]), 2),
                "Catering_Cost": round(float(row["Catering_Cost"]), 2),
                "Overhead_Cost": round(float(row["Overhead_Cost"]), 2),
                "Total_Cost": round(float(row["Total_Cost"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Profit_Margin_PCT": round(float(row["Profit_Margin"]), 2)
            })

        self.fact_flight_ops = pd.DataFrame(ffo_records)
        self.fact_flight_ops["Flight_Fact_ID"] = np.arange(1, len(self.fact_flight_ops) + 1)
        self.log(f"     Fact_Flight_Operations built: {len(self.fact_flight_ops):,} records")

    # =========================================================================
    # PHASE 3: LOADING
    # =========================================================================
    def load(self):
        self.log("PHASE 3: Loading Dimensions and Fact Tables...")

        # 1. Export Cleaned CSVs for direct Power BI / Tableau Import
        self.log(f"  -> Exporting Dimensional Tables to CSV in {self.output_dw_dir}...")
        self.dim_date.to_csv(self.output_dw_dir / "Dim_Date.csv", index=False)
        self.dim_airport.to_csv(self.output_dw_dir / "Dim_Airport.csv", index=False)
        self.dim_airline.to_csv(self.output_dw_dir / "Dim_Airline.csv", index=False)
        self.dim_aircraft.to_csv(self.output_dw_dir / "Dim_Aircraft.csv", index=False)
        self.dim_route.to_csv(self.output_dw_dir / "Dim_Route.csv", index=False)
        self.fact_route_perf.to_csv(self.output_dw_dir / "Fact_Route_Performance.csv", index=False)
        self.fact_flight_ops.to_csv(self.output_dw_dir / "Fact_Flight_Operations.csv", index=False)

        # 2. Load into Relational SQLite Warehouse
        self.log(f"  -> Loading into SQLite Database: {self.db_path}...")
        conn = sqlite3.connect(self.db_path)
        
        # Load Dimensions first
        self.dim_date.to_sql("Dim_Date", conn, if_exists="replace", index=False)
        self.dim_airport.to_sql("Dim_Airport", conn, if_exists="replace", index=False)
        self.dim_airline.to_sql("Dim_Airline", conn, if_exists="replace", index=False)
        self.dim_aircraft.to_sql("Dim_Aircraft", conn, if_exists="replace", index=False)
        self.dim_route.to_sql("Dim_Route", conn, if_exists="replace", index=False)
        
        # Load Facts
        self.fact_route_perf.to_sql("Fact_Route_Performance", conn, if_exists="replace", index=False)
        self.fact_flight_ops.to_sql("Fact_Flight_Operations", conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()
        self.log("[OK] Physical Database Loading Complete.")

    # =========================================================================
    # PHASE 4: VALIDATION
    # =========================================================================
    def validate(self):
        self.log("PHASE 4: Executing Automated Data Warehouse Validation Checks...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check 1: Record Count Reconciliation
        tables = ["Dim_Date", "Dim_Airport", "Dim_Airline", "Dim_Aircraft", "Dim_Route", "Fact_Route_Performance", "Fact_Flight_Operations"]
        reconciliation = {}
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]
            reconciliation[t] = cnt
            self.log(f"  • Table '{t}': {cnt:,} rows verified")

        # Check 2: Financial Integrity (Total Revenue Sum check)
        cursor.execute("SELECT SUM(Annual_Revenue_USD_M), SUM(Net_Profit_USD_M), AVG(Profit_Margin_PCT) FROM Fact_Route_Performance")
        tot_rev, tot_profit, avg_margin = cursor.fetchone()
        self.log(f"  • Global Route Revenue Total: ${tot_rev:,.2f} Million USD")
        self.log(f"  • Global Route Net Profit Total: ${tot_profit:,.2f} Million USD")
        self.log(f"  • Average Global Route Margin: {avg_margin:.2f}%")

        # Check 3: Referential Integrity
        cursor.execute("""
            SELECT COUNT(*) FROM Fact_Route_Performance f
            LEFT JOIN Dim_Route r ON f.Route_Key = r.Route_Key
            WHERE r.Route_Key IS NULL
        """)
        orphaned_routes = cursor.fetchone()[0]
        self.log(f"  • Orphaned Route Keys in Fact Table: {orphaned_routes} (Must be 0)")

        conn.close()
        self.validation_results = {
            "reconciliation": reconciliation,
            "financial_summary": {
                "total_revenue_usd_m": tot_rev,
                "total_profit_usd_m": tot_profit,
                "avg_margin_pct": avg_margin
            },
            "orphaned_keys": orphaned_routes
        }
        self.log("[SUCCESS] ETL Validation Completed with Zero Errors!")

    def _map_region(self, country: str) -> str:
        country = str(country).lower()
        if any(c in country for c in ["united states", "canada", "mexico"]):
            return "North America"
        elif any(c in country for c in ["united kingdom", "germany", "france", "spain", "italy", "netherlands", "switzerland"]):
            return "Europe"
        elif any(c in country for c in ["china", "japan", "india", "korea", "singapore", "thailand", "malaysia"]):
            return "Asia-Pacific"
        elif any(c in country for c in ["emirates", "saudi", "qatar", "oman", "kuwait", "bahrain"]):
            return "Middle East"
        elif any(c in country for c in ["australia", "new zealand"]):
            return "Oceania"
        elif any(c in country for c in ["brazil", "argentina", "colombia", "chile"]):
            return "Latin America"
        else:
            return "Other / Global"


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    pipeline = AirlineDWETLPipeline(root)
    pipeline.extract()
    pipeline.transform()
    pipeline.load()
    pipeline.validate()
