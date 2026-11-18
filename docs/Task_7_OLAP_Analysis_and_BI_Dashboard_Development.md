# Task 7: OLAP Analysis and Business Intelligence Dashboard Development
**Module:** IT3101 – Data Warehousing and Business Intelligence (DWBI)  
**Academic Degree:** BSc (Hons) in Information Technology / Computing (SLIIT)  
**Project Title:** Design and Implementation of a Data Warehouse and Business Intelligence Solution for Global Airline Route & Revenue Analytics (2010–2026)  
**Allocated Marks:** 15 Marks  

---

## 7.1 Overview of the Business Intelligence Solution

The analytical presentation tier is developed using **Microsoft Power BI Desktop**, connected to the Enterprise Data Warehouse Star Schema and Departmental Data Mart tables. 

The dashboard enables multidimensional Online Analytical Processing (**OLAP**) operations:
* **Slicing & Dicing:** Isolating performance by specific calendar years, geographic corridors, and route distance categories.
* **Drill-Down & Roll-Up:** Seamlessly navigating hierarchical dimensions from **Corridor Region $\longrightarrow$ Route Haul Category $\longrightarrow$ Specific Airport Pair**.
* **Dynamic Measure Evaluation:** High-speed in-memory aggregation of financial ratios (Profit Margin %, Passenger Yield, Average Ticket Fare) using optimized **DAX (Data Analysis Expressions)**.

The BI dashboard is organized into **three dedicated report pages** in strict alignment with the assignment specifications:
1. **Report Page 1: Executive Summary**
2. **Report Page 2: Trend Analysis (2015–2026)**
3. **Report Page 3: Interactive Diagnostics & Drill-Down Analysis**

---

## 7.2 Semantic Model & Core DAX Measures Catalog

To ensure dynamic, accurate calculations across any user filter selection, the following DAX measures were authored in the semantic model:

```dax
// 1. Total Global Route Revenue (USD Millions)
Total_Revenue_M = 
SUM(Fact_Route_Performance[Annual_Revenue_USD_M])

// 2. Total Global Route Operating Cost (USD Millions)
Total_Cost_M = 
SUM(Fact_Route_Performance[Operating_Cost_USD_M])

// 3. Total Net Operating Profit (USD Millions)
Total_Profit_M = 
SUM(Fact_Route_Performance[Net_Profit_USD_M])

// 4. Weighted Network Profit Margin % (Non-Additive Ratio)
Network_Margin_PCT = 
DIVIDE([Total_Profit_M], [Total_Revenue_M], 0) * 100

// 5. Total Passengers Transported (Millions)
Total_Passengers_M = 
SUM(Fact_Route_Performance[Annual_Passengers_M])

// 6. Weighted Average Passenger Fare (USD)
Avg_Passenger_Fare_USD = 
DIVIDE([Total_Revenue_M] * 1000000.0, [Total_Passengers_M] * 1000000.0, 0)

// 7. Year-over-Year (YoY) Revenue Growth %
YoY_Revenue_Growth_PCT = 
VAR CurrentRev = [Total_Revenue_M]
VAR PriorRev = CALCULATE([Total_Revenue_M], SAMEPERIODLASTYEAR(Dim_Date[Full_Date]))
RETURN
DIVIDE(CurrentRev - PriorRev, PriorRev, 0) * 100
```

---

## 7.3 Report Page 1: Executive Summary

### 1. Purpose and Design Objectives
The **Executive Summary** is designed for C-level leadership (Chief Executive Officer, Chief Commercial Officer, Chief Financial Officer). It provides a macro-level overview of global commercial health, overall profitability, passenger volume, and geographic route performance.

### 2. Layout Structure & Visual Specifications

```
+---------------------------------------------------------------------------------------------------+
|  [HEADER] Global Airline Route & Revenue Analytics — Executive Summary Dashboard (2015-2026)      |
+-------------------+--------------------+--------------------+-------------------+-----------------+
|  CARD 1: Revenue  |  CARD 2: Profit    |  CARD 3: Margin %  |  CARD 4: Pax Vol  | CARD 5: Avg Fare|
|     $209.36 B     |     $12.83 B       |       6.13%        |    1,942.5 M      |     $107.78     |
+-------------------+--------------------+--------------------+-------------------+-----------------+
|                                        |                                                          |
|  VISUAL A: Clustered Bar Chart         |  VISUAL C: Donut Chart                                   |
|  Revenue & Net Profit by Region        |  Route Performance Tier Breakdown                        |
|  • Atlantic: $68.4B Rev, $4.8B Profit  |  • Stable Contributor: 55.0%                             |
|  • Asia-Pacific: $54.2B Rev, $3.9B Prof|  • High Margin Star:   18.5%                             |
|  • Europe-ME: $36.1B Rev, $2.5B Profit |  • Low Margin Volume:  14.0%                             |
|                                        |  • Under Review / Loss:12.5%                             |
+----------------------------------------+----------------------------------------------------------+
|  VISUAL B: Bubble Map Visual                                                                      |
|  Global Airport Hub Network (Latitude, Longitude, Bubble Size = Annual Revenue USD M)            |
+---------------------------------------------------------------------------------------------------+
```

### 3. Detailed Component Breakdown:
* **Top KPI Scorecard Band:**
  * `Total_Revenue_M`: Displayed as `$209.4B` (Target: Sustainable corporate growth).
  * `Total_Profit_M`: Displayed as `$12.8B`.
  * `Network_Margin_PCT`: Displayed as `6.1%` (Aviation sector benchmark range: 5%–8%).
  * `Total_Passengers_M`: Displayed as `1.94 Billion Passengers`.
* **Visual A (Clustered Bar Chart):**  
  * *Y-Axis:* `Dim_Route[Corridor_Region]`.  
  * *X-Axis:* `[Total_Revenue_M]` and `[Total_Profit_M]`.  
  * *Insight:* Immediately highlights that the **North Atlantic Corridor (Europe $\leftrightarrow$ North America)** generates the highest aggregate dollar profit ($4.8B), followed closely by **Intra-Asia** ($3.9B).
* **Visual B (Geographic Bubble Map):**  
  * *Location:* `Dim_Airport[City], Dim_Airport[Country]`.  
  * *Coordinates:* `Dim_Airport[Latitude]`, `Dim_Airport[Longitude]`.  
  * *Bubble Size:* `[Total_Revenue_M]`.  
  * *Color:* Region category.
* **Visual C (Performance Tier Donut Chart):**  
  * *Legend:* `DM_Route_Profitability_Summary[Route_Performance_Tier]`.  
  * *Values:* Count of `Route_Code`.  
  * *Insight:* Reveals that 73.5% of monitored routes are stable or high-margin stars, while 12.5% operate with marginal or negative contributions requiring commercial intervention.

---

## 7.4 Report Page 2: Trend Analysis (2015–2026)

### 1. Purpose and Design Objectives
The **Trend Analysis** page delivers longitudinal time-series diagnostics spanning 11 years (2015 to 2026). It visualizes pre-crisis historical benchmarks, the severe pandemic disruption drop (2020–2022), the rapid recovery rebound (2023–2024), and future projected operational stabilization (2025–2026).

### 2. Layout Structure & Visual Specifications

```
+---------------------------------------------------------------------------------------------------+
|  [HEADER] Global Airline Route Network — Multi-Year Financial & Traffic Trends (2015–2026)        |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 1: Line and Clustered Column Chart                                                        |
|  11-Year Trajectory: Total Revenue ($M), Operating Cost ($M) vs Operating Margin %                |
|  [Columns: Revenue (Blue), Cost (Gray) | Line: Net Margin % (Orange)]                             |
|  2015: $18.2B Rev (8.2% Margin)                                                                   |
|  2020: $3.7B Rev (-32.5% Margin Crisis Dip)                                                       |
|  2024: $28.4B Rev (6.8% Post-Recovery)                                                            |
|  2026: $33.4B Rev (7.4% Steady Expansion)                                                         |
+---------------------------------------------------+-----------------------------------------------+
|  VISUAL 2: Dual-Axis Line Chart                   |  VISUAL 3: Multi-Line Trend Chart             |
|  Passenger Volume vs Average Ticket Fare Trend    |  Top 5 Revenue Corridors Trajectory           |
|  • Passengers (M) on primary Y-axis               |  • London-New York (LHR-JFK)                  |
|  • Avg Ticket Fare ($) on secondary Y-axis        |  • Tokyo-Singapore (HND-SIN)                  |
|  (Reveals fare inflation from $65 to $88)         |  • Dubai-London (DXB-LHR)                     |
|                                                   |  • Melbourne-Sydney (MEL-SYD)                 |
+---------------------------------------------------+-----------------------------------------------+
```

### 3. Detailed Component Breakdown:
* **Visual 1 (Line and Clustered Column Chart):**
  * *Shared X-Axis:* `Dim_Date[Year]` (2015, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026).
  * *Column Y-Axis:* `[Total_Revenue_M]` and `[Total_Cost_M]`.
  * *Line Y-Axis:* `[Network_Margin_PCT]`.
  * *Analytical Value:* Highlights operational resilience: revenues collapsed by over 79% in 2020 before surpassing pre-pandemic levels by 2023, with projected revenue hitting $33.4B in 2026.
* **Visual 2 (Passenger Volume vs. Average Fare Trend):**
  * *X-Axis:* `Dim_Date[Year]`.
  * *Primary Y-Axis (Line 1):* `[Total_Passengers_M]`.
  * *Secondary Y-Axis (Line 2):* `[Avg_Passenger_Fare_USD]`.
  * *Analytical Value:* Confirms that fare inflation post-2022 was readily absorbed by travelers without depressing passenger volume demand.
* **Visual 3 (Top 5 Corridors Revenue Evolution):**
  * *X-Axis:* `Dim_Date[Year]`.
  * *Y-Axis:* `[Total_Revenue_M]`.
  * *Legend:* `Dim_Route[Route_Name]` (Filtered for Top 5 Corridors).
  * *Analytical Value:* Illustrates that London–New York (`LHR-JFK`) consistently remains the world's most lucrative commercial airline corridor, breaking $1.47 Billion USD annually by 2026.

---

## 7.5 Report Page 3: Interactive Diagnostics & Drill-Down Analysis

### 1. Purpose and Design Objectives
The **Interactive Analysis** page is the investigative workbench for Route Planners and Commercial Pricing Analysts. It enables users to dynamically filter by corridor region, haul category, and calendar year, and drill down through dimensional hierarchies.

### 2. Layout Structure & Visual Specifications

```
+---------------------------------------------------------------------------------------------------+
|  [SLICER BAR] Year: [All / 2024 / 2025 / 2026] | Region: [Dropdown] | Route Haul: [Long/Med/Short]|
+---------------------------------------------------------------------------------------------------+
|  VISUAL A: Hierarchical Matrix with Expandable Drill-Down (+)                                     |
|  Hierarchy: Region  -->  Route Category (Haul)  -->  Specific Route Corridor                      |
|  Columns: Revenue ($M) | Operating Cost ($M) | Net Profit ($M) | Margin % | Weekly Freq | Yield   |
|  [+] Atlantic                                                                                     |
|      [+] Long Haul                                                                                |
|          London-New York (LHR-JFK): $1,475.2M Rev | $103.3M Profit | 7.00% Margin | 42 Freq       |
|          Paris-New York (CDG-JFK):  $920.4M Rev   | $64.4M Profit  | 7.00% Margin | 28 Freq       |
+---------------------------------------------------------------------------------------------------+
|  VISUAL B: Exception Table (Alerts)               |  VISUAL C: Fleet Efficiency Scatter Plot      |
|  Underperforming Routes Watchlist (Margin < 2%)   |  Seat Load Factor % vs Fuel Cost Share %      |
|  • Route Code, Route Name, Revenue, Profit, Margin|  • Wide-Body vs Narrow-Body Fleet Clusters    |
|  • Conditional Formatting: Red Alert on Negatives |                                               |
+---------------------------------------------------+-----------------------------------------------+
```

### 3. Detailed Component Breakdown:
* **Interactive Slicers:**
  * Slicer 1: `Dim_Date[Year]` (Buttons: 2015 to 2026).
  * Slicer 2: `Dim_Route[Corridor_Region]` (Multi-select dropdown).
  * Slicer 3: `Dim_Route[Route_Category]` (`Long Haul`, `Medium Haul`, `Short Haul`).
* **Visual A (Hierarchical Matrix with Drill-Down):**
  * *Rows (Hierarchy):* `Dim_Route[Corridor_Region]` $\longrightarrow$ `Dim_Route[Route_Category]` $\longrightarrow$ `Dim_Route[Route_Name]`.
  * *Values:* `[Total_Revenue_M]`, `[Total_Cost_M]`, `[Total_Profit_M]`, `[Network_Margin_PCT]`, `[Avg_Passenger_Fare_USD]`.
  * *OLAP Operation:* Users can click the `(+)` expansion icon to drill down from broad geographic regions into individual route-level yield metrics.
* **Visual B (Exception Alert Table):**
  * Sourced from `DM_Underperforming_Routes_Watchlist`.
  * Contains conditional formatting: cells with negative net profit or margins below 2.0% are highlighted with a soft red fill.
* **Visual C (Fleet Efficiency Scatter Plot):**
  * *X-Axis:* `Avg_Load_Factor_PCT` (Seat Occupancy).
  * *Y-Axis:* `Fuel_Cost_Share_PCT` (% of Total Cost driven by Jet Fuel).
  * *Legend:* `Body_Type` (`Wide-Body` vs `Narrow-Body`).
  * *Insight:* Demonstrates that wide-body aircraft deployed with load factors below 72% suffer severe margin compression due to fixed fuel burn penalties.
