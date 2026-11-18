# Task 6: Data Mart Development
**Module:** IT3101 – Data Warehousing and Business Intelligence (DWBI)  
**Academic Degree:** BSc (Hons) in Information Technology / Computing (SLIIT)  
**Project Title:** Design and Implementation of a Data Warehouse and Business Intelligence Solution for Global Airline Route & Revenue Analytics (2010–2026)  
**Allocated Marks:** 10 Marks  

---

## 6.1 Purpose of the Departmental Data Mart

In an enterprise data warehousing ecosystem, an Enterprise Data Warehouse (EDW) holds a broad, normalized, or cross-functional view of the entire organization. However, operational business units—such as Commercial Route Planning and Revenue Management—require fast, focused, and domain-specific analytical access without navigating complex multi-table joins across hundreds of columns.

To address this need, the **Route Profitability and Commercial Revenue Management Data Mart** was designed and implemented.

```
+-----------------------------------------------------------------------------------+
|                        ENTERPRISE DATA WAREHOUSE (EDW)                            |
|             (Full Star Schema: Facts, Conformed Dimensions, Millions of Rows)     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼  (Focused Extraction & Pre-Aggregation)
+-----------------------------------------------------------------------------------+
|        ROUTE PROFITABILITY & COMMERCIAL REVENUE MANAGEMENT DATA MART              |
|                                                                                   |
|  • Pre-aggregated Route Margin Cubes           • Regional Corridor Benchmarks     |
|  • Underperforming Route Early Warning View    • Fleet Fuel & Yield Efficiency    |
+-----------------------------------------------------------------------------------+
```

### Core Objectives of the Data Mart:
1. **Isolate Route Margin Drivers:** Provide commercial strategists with pre-calculated profit, cost, and passenger yield figures for every major global corridor from 2015 through 2026.
2. **Early Detection of Loss-Making Corridors:** Automatically segment routes into performance tiers (`High Margin Star`, `Stable Contributor`, `Low Margin Volume`, `Loss Making / Under Review`) to trigger timely network restructuring.
3. **Fleet Allocation Guidance:** Correlate seat capacity, load factors, and fuel expenses by aircraft type to ensure that wide-body aircraft (e.g., Airbus A380, Boeing 777) are deployed exclusively on high-density, profitable corridors.

---

## 6.2 Target Users and Business Personas

The Data Mart is customized specifically for decision-makers within the airline's Commercial and Operations divisions:

| User Persona | Department | Primary Business Questions Answered | Key Metrics Monitored |
| :--- | :--- | :--- | :--- |
| **Chief Commercial Officer (CCO)** | Executive Leadership | • What is our total network revenue and net profit across global corridors?<br>• Which international regions deliver the highest profit margin %? | Total Network Revenue ($M), Net Profit ($M), Operating Margin %, Passenger Volume |
| **Network Planning Director** | Network Strategy | • Which routes should we expand, reduce in weekly frequency, or suspend?<br>• Are high-traffic routes actually profitable after accounting for airport tariffs? | Weekly Flight Frequency, Route Distance, Corridor Region, Route Margin Tier |
| **Route Pricing & Yield Analyst** | Revenue Management | • Is ticket fare yield keeping pace with inflationary fuel costs?<br>• How do seasonal peaks impact passenger demand and average fares? | Average Ticket Fare ($), Derived Yield per Passenger ($), Load Factor % |
| **Fleet Operations Manager** | Flight Operations | • Which aircraft models operate with the lowest fuel expense share?<br>• Is aircraft seating capacity being wasted on low-demand corridors? | Fuel Cost Share %, Total Flights Operated, Aircraft Seating Capacity |

---

## 6.3 Physical Implementation and Schema Structure

The Data Mart is physically deployed within the warehouse database ([`data/warehouse/airline_dw.db`](file:///c:/Users/union/Desktop/DWBI_P/data/warehouse/airline_dw.db)) and exported as clean analytical structures ([`data/warehouse/`](file:///c:/Users/union/Desktop/DWBI_P/data/warehouse)):

### 1. `DM_Route_Profitability_Summary` (Executive Route Cube)
* **Underlying Query / Grain:** One row per airline route corridor per calendar year (400 records, 2015–2026).
* **Key Columns:** `Year`, `Route_Code`, `Route_Name`, `Corridor_Region`, `Route_Category`, `Distance_KM`, `Origin_City`, `Destination_City`, `Annual_Revenue_USD_M`, `Operating_Cost_USD_M`, `Net_Profit_USD_M`, `Profit_Margin_PCT`, `Annual_Passengers_M`, `Avg_Fare_USD`, `Weekly_Frequency_Est`, `Derived_Yield_Per_Pax`, `Route_Performance_Tier`.
* **Business Logic:** Automatically categorizes routes into four strategic performance bands based on profit margin percentage.

### 2. `DM_Regional_Corridor_Performance` (Macro-Regional Aggregation)
* **Underlying Query / Grain:** One row per geographic corridor region per calendar year (140 records).
* **Key Columns:** `Year`, `Corridor_Region`, `Total_Active_Routes`, `Regional_Revenue_USD_M`, `Regional_Operating_Cost_USD_M`, `Regional_Net_Profit_USD_M`, `Weighted_Regional_Margin_PCT`, `Total_Regional_Passengers_M`, `Avg_Regional_Ticket_Fare_USD`.
* **Business Logic:** Computes weighted profit margins across multi-route corridors (e.g., North Atlantic, Intra-Asia, Europe-Middle East) to support regional resource allocation.

### 3. `DM_Underperforming_Routes_Watchlist` (Diagnostic Exception View)
* **Underlying Query / Grain:** Filtered subset of routes experiencing margin erosion (`Net_Profit_USD_M < 0` or `Profit_Margin_PCT < 2.0%`).
* **Key Columns:** `Year`, `Route_Code`, `Route_Name`, `Corridor_Region`, `Annual_Revenue_USD_M`, `Operating_Cost_USD_M`, `Net_Profit_USD_M`, `Profit_Margin_PCT`, `Avg_Fare_USD`.
* **Business Logic:** Acts as an operational early-warning alert system for network planners to review unprofitable flight sectors.

### 4. `DM_Aircraft_Fleet_Efficiency` (Equipment Economics Mart)
* **Underlying Query / Grain:** One row per commercial aircraft model variant.
* **Key Columns:** `Manufacturer`, `Aircraft_Model_Name`, `Body_Type`, `Total_Flights_Operated`, `Avg_Load_Factor_PCT`, `Total_Fleet_Revenue`, `Total_Fleet_Cost`, `Total_Fleet_Net_Profit`, `Fleet_Profit_Margin_PCT`, `Total_Fuel_Expense`, `Fuel_Cost_Share_PCT`.
* **Business Logic:** Decomposes flight expenses to determine fuel burn proportions and unit margins for fleet deployment decisions.

---

## 6.4 Sample Data Mart Output Evidence

Below is an extract from the physical Data Mart view [`DM_Route_Profitability_Summary`](file:///c:/Users/union/Desktop/DWBI_P/data/warehouse/DM_Route_Profitability_Summary.csv) demonstrating real analytical records:

```text
Year | Route_Code | Route_Name       | Region        | Revenue ($M) | Cost ($M) | Profit ($M) | Margin % | Tier
-----+------------+------------------+---------------+--------------+-----------+-------------+----------+--------------------
2024 | CJU-GMP    | Jeju-Seoul       | Asia          | $550.30      | $495.27   | $55.03      | 10.00%   | Stable Contributor
2024 | HND-CTS    | Tokyo-Sapporo    | Asia          | $367.10      | $330.39   | $36.71      | 10.00%   | Stable Contributor
2024 | MEL-SYD    | Melbourne-Sydney | Oceania       | $529.00      | $476.10   | $52.90      | 10.00%   | Stable Contributor
2024 | LHR-JFK    | London-New York  | Atlantic      | $1,153.20    | $1,072.48 | $80.72      |  7.00%   | Stable Contributor
2024 | DXB-LHR    | Dubai-London     | Europe-ME     | $873.30      | $812.17   | $61.13      |  7.00%   | Stable Contributor
2025 | LHR-JFK    | London-New York  | Atlantic      | $1,348.80    | $1,254.38 | $94.42      |  7.00%   | Stable Contributor
2026 | LHR-JFK    | London-New York  | Atlantic      | $1,475.20    | $1,371.94 | $103.26     |  7.00%   | Stable Contributor
```

---

## 6.5 Analytical Benefits of the Data Mart

The creation of the **Route Profitability and Revenue Management Data Mart** provides four substantial analytical advantages:

1. **Sub-Second Analytical Query Performance:**  
   By pre-joining dimension tables (Airports, Routes, Dates) and pre-calculating financial ratios (`Profit_Margin_PCT`, `Yield_Per_Pax`, `Fuel_Cost_Share_PCT`), analytical queries and Power BI visuals render instantaneously, avoiding expensive runtime table scans.

2. **Domain-Specific Business Logic Encapsulation:**  
   Complex aviation business rules (such as performance tiering and weighted regional margin formulas) are codified directly within the SQL views. This ensures that all pricing analysts and network planners work with identical definitions of profitability.

3. **Optimized for BI Consumption:**  
   The Data Mart views feed directly into Power BI's reporting layer without requiring complex multi-table relationship modeling in DAX, reducing semantic model complexity and memory overhead.

4. **Data Security and Role-Based Access Control:**  
   In a production enterprise environment, the Data Mart allows the airline to grant commercial planners access to revenue, fare, and margin metrics while restricting access to sensitive corporate payroll or aircraft lease contract data residing in the broader EDW.
