# Task 1: Dataset Selection and Business Scenario Identification
**Module:** IT3101 – Data Warehousing and Business Intelligence (DWBI)  
**Academic Degree:** BSc (Hons) in Information Technology / Computing (SLIIT)  
**Project Title:** Design and Implementation of a Data Warehouse and Business Intelligence Solution for Global Airline Route & Revenue Analytics (2010–2026)  
**Allocated Marks:** 10 Marks  

---

## 1.1 Business Domain Overview

The selected business domain is **Commercial Aviation and Global Airline Transportation**. The commercial airline industry operates in an intensely competitive, capital-intensive, and volatile macroeconomic environment characterized by tight operating margins (historically between 3% and 9%), dynamic customer demand, fluctuating jet fuel costs, and complex global regulatory tariffs. 

Modern international airlines and aviation alliances manage extensive route networks connecting hundreds of international hubs and regional spokes. To sustain commercial viability, airline executives, network planners, and revenue management departments must continuously monitor flight-level and route-level financial performance, passenger load factors, cost decompositions, and fleet efficiency across diverse geographic corridors.

---

## 1.2 Purpose of the Operational (OLTP) System

In a real-world aviation enterprise, operational data originates from disparate **Online Transaction Processing (OLTP)** systems:
1. **Flight Operations & Dispatch System (FODS):** Records scheduled vs. actual flight departures, aircraft tail assignments, block hours, nautical distance flown, and route waypoints.
2. **Passenger Service & Reservation System (PSS / GDS):** Captures passenger bookings, ticketing fares, cabin class distribution (First, Business, Premium Economy, Economy), and ancillary purchases (baggage fees, priority boarding, seat selection).
3. **Flight Cost Accounting & Fuel Tracking System:** Tracks direct operating costs (DOC) per flight leg, including jet fuel burn, maintenance reserves, flight and cabin crew compensation, airport landing fees, air navigation service charges, ground handling, and in-flight catering.
4. **Fleet & Hub Infrastructure Registry:** Maintains master metadata concerning aircraft specifications (seat capacity, engine variant, maximum take-off weight) and airport facilities (IATA/ICAO codes, geographic coordinates, runway limits, terminal tariffs).

The operational system's primary purpose is day-to-day transaction processing: ticketing passengers, dispatching aircraft, tracking fuel, and invoicing fees. However, these OLTP databases are highly normalized (3NF), optimized for rapid row-level write throughput, and siloed across operational departments—rendering them inefficient and unsuitable for complex multi-year analytical queries, cross-regional aggregations, or executive reporting.

---

## 1.3 Business Problem Addressed

Global aviation executives and network strategists face critical decision-making challenges that cannot be resolved using operational transactional systems alone:

1. **Route Profitability and Margin Volatility:**
   Airlines often maintain high passenger traffic volumes on popular international routes while silently losing money due to disproportionate airport tariffs, high fuel burn on long flight sectors, or excessive ground handling fees. Management lacks a unified multidimensional platform to distinguish high-yield profit corridors from loss-making prestige routes.

2. **Suboptimal Capacity & Fleet Allocation:**
   Deploying the wrong aircraft type on a route leads to either missed revenue (spillover demand on capacity-constrained flights) or devastating unit costs (flying high-capacity wide-body aircraft like the Airbus A380 or Boeing 777-300ER with poor load factors). Planners need analytical visibility into seat utilization across seasonal peaks and troughs.

3. **Cost Decomposition & Inflationary Pressures:**
   Operating expenses—specifically jet fuel, navigation charges, and maintenance reserves—fluctuate unpredictably across global regions. Management requires granular cost attribution to identify whether cost overruns stem from fuel price shocks, airport landing fee hikes, or crew scheduling inefficiencies.

4. **Multi-Year Macro Disruption and Recovery Dynamics (2010–2026):**
   Between 2010 and 2026, the global aviation sector experienced major structural disruptions: macroeconomic cycles, the 737 MAX groundings, the post-pandemic recovery surge, and subsequent supply chain bottlenecks. Decision-makers require historical trend benchmarks and multi-year comparative views to forecast capacity and re-route corridors effectively.

---

## 1.4 Dataset Source and Authenticity

To model this enterprise business scenario realistically and rigorously, the solution utilizes a curated, multidimensional aviation dataset acquired from authoritative international aviation repositories:

* **Primary Analytical Source:** *Global Aviation Industry (2010–2026)*  
  * **Provider / Curator:** Sergey Nefedov (Aviation Industry Data Repository, Kaggle).  
  * **Coverage:** 17 years (2010 through 2026).  
  * **Originating Industry Sources:** Compiled from official International Air Transport Association (**IATA**) World Air Transport Statistics, International Civil Aviation Organization (**ICAO**) traffic reporting forms, airline Form 41 financial schedules, and manufacturer order books (Boeing and Airbus commercial delivery databases).
* **Operational Flight-Level Source:** *Airline Route Profitability & Cost Decomposition*  
  * **Provider / Curator:** Waleed Faheem (Kaggle).  
  * **Nature:** Detailed transactional flight operations log capturing 33 operational, cost, and revenue variables per flight leg.
* **Master Dimensional Reference:** *OpenFlights Aeronautical Infrastructure Database (Update 2024)*  
  * **Curator:** Ahmad Rafiee (OpenFlights.org / Kaggle).  
  * **Contents:** Comprehensive master records for worldwide airports, airline carriers, aircraft equipment, and global route networks.

---

## 1.5 Dataset Format and Scale (Record Counts)

The dataset encompasses a multi-table relational schema containing **77,000+ total records** across both historical longitudinal series and granular transactional logs:

| Dataset / Table Name | Source File Format | Record Count (Rows) | Attributes (Cols) | Physical Size | Temporal Range |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Route Performance** (`route_performance.csv`) | Comma-Separated Values | **400** | 11 | 34.4 KB | **2015 – 2026** |
| **Airline Financials** (`airline_financials.csv`) | Comma-Separated Values | **497** | 12 | 34.2 KB | **2010 – 2026** |
| **Passenger Traffic** (`passenger_traffic.csv`) | Comma-Separated Values | **1,176** | 7 | 49.9 KB | **2010 – 2026** |
| **Fleet Orders & Backlog** (`fleet_orders.csv`) | Comma-Separated Values | **86** | 10 | 3.9 KB | **2010 – 2026** |
| **Operational Flight Logs** (`airline_route_profitability.csv`) | Comma-Separated Values | **7,974** | 33 | 1.98 MB | **2024** |
| **Airport Master Directory** (`airports.csv`) | Comma-Separated Values | **7,698** | 14 | 979.4 KB | Master / Static |
| **Airline Carrier Directory** (`airlines.csv`) | Comma-Separated Values | **6,162** | 8 | 314.5 KB | Master / Static |
| **Aircraft Model Specifications** (`airplanes.csv`) | Comma-Separated Values | **246** | 3 | 6.8 KB | Master / Static |
| **Global Route Network Connections** (`routes.csv`) | Comma-Separated Values | **67,663** | 9 | 2.25 MB | Master / Static |

---

## 1.6 Attributes Description (Data Dictionary)

The operational datasets feature diverse numerical, categorical, temporal, and spatial attributes that naturally partition into dimensional models:

### 1. Route Performance Attributes (`route_performance.csv`)
* `year` *(Integer)*: Calendar year of operational reporting (2015 to 2026).
* `route` *(Text)*: Origin and destination city pair designation (e.g., "London-New York", "Jeju-Seoul", "Dubai-London").
* `origin_iata` *(Text [3])*: Three-letter IATA code for the departure hub (e.g., LHR, DXB, JFK).
* `destination_iata` *(Text [3])*: Three-letter IATA code for the arrival hub (e.g., JFK, LHR, CDG).
* `distance_km` *(Float)*: Great-circle flight route distance in kilometers.
* `region` *(Categorical)*: Geographic corridor classification (Asia, North America, Atlantic, Europe, Middle East, Pacific, Oceania, Latin America).
* `main_airlines` *(Text)*: Key competing carriers operating the corridor (e.g., "British Airways, Virgin Atlantic, American Airlines").
* `annual_passengers_m` *(Float - Measure)*: Total passengers transported on the route per annum (in millions).
* `avg_fare_usd` *(Float - Measure)*: Weighted average passenger ticket fare in USD.
* `weekly_frequency_est` *(Integer - Measure)*: Average weekly scheduled flight frequency.
* `annual_revenue_usd_m` *(Float - Measure)*: Total gross route revenue generated per annum (in millions USD).

### 2. Airline Corporate Financial Attributes (`airline_financials.csv`)
* `year` *(Integer)*: Financial reporting fiscal year (2010 to 2026).
* `airline_name` *(Text)*: Commercial airline operating entity (e.g., Delta Air Lines, Emirates, Singapore Airlines, Lufthansa).
* `iata_code` *(Text [2/3])*: Standard airline carrier code (e.g., DL, EK, SQ, LH).
* `country_iso3` *(Text [3])*: Country of incorporation (USA, ARE, SGP, DEU).
* `region` *(Text)*: Operating continent/region.
* `business_model` *(Categorical)*: Carrier commercial model (`legacy` network carrier vs. `low_cost` budget carrier).
* `revenue_usd_bn` *(Float - Measure)*: Annual corporate operating revenue in billions USD.
* `operating_margin_pct` *(Float - Measure)*: Operating profit margin percentage ($\frac{\text{Operating Profit}}{\text{Revenue}} \times 100$).
* `operating_income_usd_bn` *(Float - Measure)*: Operating profit before taxes and interest in billions USD.
* `passengers_carried_m` *(Float - Measure)*: Total systemwide annual passenger volume (in millions).
* `load_factor_pct` *(Float - Measure)*: Ratio of revenue passenger kilometers to available seat kilometers.
* `fleet_size_est` *(Integer - Measure)*: Number of active commercial aircraft in operating fleet.

### 3. Flight-Level Cost & Revenue Breakdown (`airline_route_profitability.csv`)
* **Identifiers & Operations:** `Flight_Number`, `Flight_Date`, `Origin`, `Destination`, `Route`, `Aircraft_Type`, `Aircraft_Capacity`, `Passengers`, `Load_Factor`, `Flight_Hours`, `Season` (Peak, Shoulder, Low), `Route_Category` (Long Haul, Medium Haul, Short Haul), `Demand_Level`.
* **Revenue Metrics:** `Ticket_Revenue`, `Ancillary_Revenue`, `Total_Revenue`.
* **Direct & Operating Costs:** `Fuel_Cost`, `Maintenance_Cost`, `Crew_Cost`, `Depreciation_Cost`, `Insurance_Cost`, `Airport_Fees`, `Catering_Cost`, `Handling_Cost`, `Navigation_Fees`, `Sales_Distribution_Cost`, `Passenger_Service_Cost`, `Overhead_Cost`, `Marketing_Cost`, `IT_Systems_Cost`, `Total_Cost`.
* **Profitability Measures:** `Profit`, `Profit_Margin`.

### 4. Master Dimension Attributes (`airports.csv`, `airlines.csv`, `airplanes.csv`)
* **Airports:** `Airport ID`, `Name`, `City`, `Country`, `IATA`, `ICAO`, `Latitude`, `Longitude`, `Altitude`, `Timezone`.
* **Airlines:** `Airline ID`, `Name`, `IATA`, `ICAO`, `Callsign`, `Country`, `Active`.
* **Airplanes:** `Aircraft Name`, `IATA code`, `ICAO code`.

---

## 1.7 Justification for Data Warehouse and BI Suitability

The selected dataset is ideally aligned with Data Warehousing and Business Intelligence requirements for the following technical and architectural reasons:

1. **True Representation of an Operational (OLTP) Environment:**  
   The dataset replicates the transaction schemas generated by modern airline flight dispatch and reservation systems, exhibiting real-world characteristics such as normalized codes, operational timestamps, passenger manifests, and itemized airport fee structures.

2. **High Scale and Statistical Robustness:**  
   With over **77,000+ total rows** across 10 tables and continuous longitudinal metrics spanning **17 years (2010–2026)**, the data provides sufficient depth for meaningful historical aggregations, time-series trend analysis, and OLAP processing without risk of sample bias.

3. **Natural Multi-Dimensional Fit (Star / Snowflake Schema):**  
   The data exhibits a clean, unambiguous separation between **numerical business facts** and **descriptive dimensions**:
   * **Fact Measures:** Flight revenue, ancillary fees, direct fuel expense, operating profit, profit margin, passenger volume, seat capacity, load factor, and average fare.
   * **Dimensions:** Date/Time (`Dim_Date`), Route corridor (`Dim_Route`), Departure/Arrival Airports (`Dim_Airport`), Aircraft equipment (`Dim_Aircraft`), Airline carrier (`Dim_Airline`), and Cabin/Service class (`Dim_Service`).

4. **Rich Analytical Hierarchy Support:**  
   The dimensions support natural business drill-down and roll-up paths essential for OLAP analysis:
   * *Temporal Hierarchy:* Year $\rightarrow$ Quarter $\rightarrow$ Month $\rightarrow$ Date.
   * *Geographic Hierarchy:* Global Region $\rightarrow$ Country $\rightarrow$ City $\rightarrow$ Specific Airport Hub (IATA).
   * *Route Hierarchy:* Route Category (Long/Medium/Short Haul) $\rightarrow$ Specific City Pair Corridor $\rightarrow$ Flight Leg.
   * *Fleet Hierarchy:* Manufacturer (Boeing, Airbus) $\rightarrow$ Aircraft Family $\rightarrow$ Specific Model Variant.

5. **Direct Alignment with Executive Decision-Making (Task 7 & 8):**  
   The attributes empower interactive dashboarding in Power BI / Tableau:
   * Executive KPIs: Total Global Revenue, Average Route Profit Margin, Network-Wide Load Factor.
   * Time-series trend visuals comparing pre-pandemic, recovery, and recent 2024–2026 performance.
   * Deep-dive diagnostics revealing why certain routes suffer margin erosion despite heavy passenger volumes.
