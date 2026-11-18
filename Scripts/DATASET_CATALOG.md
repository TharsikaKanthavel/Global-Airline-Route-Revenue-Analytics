# Global Airline Route & Revenue Analytics (2010–2026)
## Technical Dataset Catalog & Audit Report

**Generated on:** 2026-09-26  
**Total CSV Data Files Audited:** 10  

### 1. High-Level Summary Table

| File Name | Path | Rows | Columns | Size (KB) | Temporal Coverage |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `airlines.csv` | `data/airports_airlines_planes/airlines.csv` | 6,162 | 8 | 314.47 KB | N/A |
| `airplanes.csv` | `data/airports_airlines_planes/airplanes.csv` | 246 | 3 | 6.77 KB | N/A |
| `airports.csv` | `data/airports_airlines_planes/airports.csv` | 7,698 | 14 | 979.36 KB | N/A |
| `routes.csv` | `data/airports_airlines_planes/routes.csv` | 67,663 | 9 | 2255.47 KB | N/A |
| `airline_financials.csv` | `data/global_aviation_2010_2026/airline_financials.csv` | 497 | 12 | 34.25 KB | 2010 - 2026 |
| `aviation_incidents.csv` | `data/global_aviation_2010_2026/aviation_incidents.csv` | 40 | 15 | 4.81 KB | 2010-04-10 to 2026-02-15 |
| `fleet_orders.csv` | `data/global_aviation_2010_2026/fleet_orders.csv` | 86 | 10 | 3.93 KB | 2010 - 2026 |
| `passenger_traffic.csv` | `data/global_aviation_2010_2026/passenger_traffic.csv` | 1,176 | 7 | 49.87 KB | 2010 - 2026 |
| `route_performance.csv` | `data/global_aviation_2010_2026/route_performance.csv` | 400 | 11 | 34.4 KB | 2015 - 2026 |
| `airline_route_profitability.csv` | `data/route_profitability/airline_route_profitability.csv` | 7,974 | 33 | 1982.16 KB | 2024-01-01 to 2024-12-31 |


### 2. Detailed Attribute Breakdown

#### `airlines.csv`
- **Path:** `data/airports_airlines_planes/airlines.csv`
- **Record Count:** 6,162 rows
- **Column Count:** 8 columns
- **Coverage:** N/A

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `Airline ID` | `int64` | 0 | -1 |
| `Name` | `object` | 0 | Unknown |
| `Alias` | `object` | 506 | \N |
| `IATA` | `object` | 4627 | - |
| `ICAO` | `object` | 87 | GNL |
| `Callsign` | `object` | 808 | \N |
| `Country` | `object` | 15 | \N |
| `Active` | `object` | 0 | Y |

---

#### `airplanes.csv`
- **Path:** `data/airports_airlines_planes/airplanes.csv`
- **Record Count:** 246 rows
- **Column Count:** 3 columns
- **Coverage:** N/A

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `Name` | `object` | 0 | Aerospatiale (Nord) 262 |
| `IATA code` | `object` | 0 | ND2 |
| `ICAO code` | `object` | 0 | N262 |

---

#### `airports.csv`
- **Path:** `data/airports_airlines_planes/airports.csv`
- **Record Count:** 7,698 rows
- **Column Count:** 14 columns
- **Coverage:** N/A

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `Airport ID` | `int64` | 0 | 1 |
| `Name` | `object` | 0 | Goroka Airport |
| `City` | `object` | 49 | Goroka |
| `Country` | `object` | 0 | Papua New Guinea |
| `IATA` | `object` | 0 | GKA |
| `ICAO` | `object` | 0 | AYGA |
| `Latitude` | `float64` | 0 | -6.0816898345900015 |
| `Longitude` | `float64` | 0 | 145.391998291 |
| `Altitude` | `int64` | 0 | 5282 |
| `Timezone` | `object` | 0 | 10 |
| `DST` | `object` | 0 | U |
| `Tz database time zone` | `object` | 0 | Pacific/Port_Moresby |
| `Type` | `object` | 0 | airport |
| `Source` | `object` | 0 | OurAirports |

---

#### `routes.csv`
- **Path:** `data/airports_airlines_planes/routes.csv`
- **Record Count:** 67,663 rows
- **Column Count:** 9 columns
- **Coverage:** N/A

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `Airline` | `object` | 0 | 2B |
| `Airline ID` | `object` | 0 | 410 |
| `Source airport` | `object` | 0 | AER |
| `Source airport ID` | `object` | 0 | 2965 |
| `Destination airport` | `object` | 0 | KZN |
| `Destination airport ID` | `object` | 0 | 2990 |
| `Codeshare` | `object` | 53066 | Y |
| `Stops` | `int64` | 0 | 0 |
| `Equipment` | `object` | 18 | CR2 |

---

#### `airline_financials.csv`
- **Path:** `data/global_aviation_2010_2026/airline_financials.csv`
- **Record Count:** 497 rows
- **Column Count:** 12 columns
- **Coverage:** 2010 - 2026

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `year` | `int64` | 0 | 2010 |
| `airline_name` | `object` | 0 | Delta Air Lines |
| `iata_code` | `object` | 0 | DAL |
| `country_iso3` | `object` | 0 | USA |
| `region` | `object` | 0 | North America |
| `business_model` | `object` | 0 | legacy |
| `revenue_usd_bn` | `float64` | 0 | 32.09 |
| `operating_margin_pct` | `float64` | 0 | 3.4 |
| `operating_income_usd_bn` | `float64` | 0 | 1.09 |
| `passengers_carried_m` | `float64` | 0 | 48.1 |
| `load_factor_pct` | `float64` | 0 | 84.5 |
| `fleet_size_est` | `int64` | 0 | 160 |

---

#### `aviation_incidents.csv`
- **Path:** `data/global_aviation_2010_2026/aviation_incidents.csv`
- **Record Count:** 40 rows
- **Column Count:** 15 columns
- **Coverage:** 2010-04-10 to 2026-02-15

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `incident_id` | `object` | 0 | AV001 |
| `date` | `object` | 0 | 2010-04-10 |
| `year` | `int64` | 0 | 2010 |
| `month` | `int64` | 0 | 4 |
| `flight_number` | `object` | 0 | PLF101 |
| `airline` | `object` | 0 | Polish AF |
| `aircraft_type` | `object` | 0 | Tu-154 |
| `severity` | `object` | 0 | fatal_crash |
| `fatalities` | `int64` | 0 | 96 |
| `location` | `object` | 0 | Smolensk, Russia |
| `description` | `object` | 0 | Polish presidential plane crash |
| `is_fatal` | `int64` | 0 | 1 |
| `is_geopolitical` | `int64` | 0 | 0 |
| `is_boeing` | `int64` | 0 | 0 |
| `is_airbus` | `int64` | 0 | 0 |

---

#### `fleet_orders.csv`
- **Path:** `data/global_aviation_2010_2026/fleet_orders.csv`
- **Record Count:** 86 rows
- **Column Count:** 10 columns
- **Coverage:** 2010 - 2026

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `year` | `int64` | 0 | 2010 |
| `manufacturer` | `object` | 0 | Airbus |
| `aircraft_family` | `object` | 0 | A320 family |
| `orders_gross` | `int64` | 0 | 452 |
| `orders_net` | `int64` | 0 | 452 |
| `deliveries` | `int64` | 0 | 401 |
| `backlog_end_of_year` | `int64` | 0 | 2440 |
| `is_widebody` | `int64` | 0 | 0 |
| `is_narrowbody` | `int64` | 0 | 1 |
| `is_regional` | `int64` | 0 | 0 |

---

#### `passenger_traffic.csv`
- **Path:** `data/global_aviation_2010_2026/passenger_traffic.csv`
- **Record Count:** 1,176 rows
- **Column Count:** 7 columns
- **Coverage:** 2010 - 2026

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `year_month` | `object` | 0 | 2010-01 |
| `year` | `int64` | 0 | 2010 |
| `month` | `int64` | 0 | 1 |
| `region` | `object` | 0 | North America |
| `rpk_billions` | `float64` | 0 | 61.73 |
| `ask_billions` | `float64` | 0 | 76.45 |
| `load_factor_pct` | `float64` | 0 | 80.8 |

---

#### `route_performance.csv`
- **Path:** `data/global_aviation_2010_2026/route_performance.csv`
- **Record Count:** 400 rows
- **Column Count:** 11 columns
- **Coverage:** 2015 - 2026

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `year` | `int64` | 0 | 2015 |
| `route` | `object` | 0 | Jeju-Seoul |
| `origin_iata` | `object` | 0 | CJU |
| `destination_iata` | `object` | 0 | GMP |
| `distance_km` | `int64` | 0 | 451 |
| `region` | `object` | 0 | Asia |
| `main_airlines` | `object` | 0 | Korean Air, Asiana, JeJu Air |
| `annual_passengers_m` | `float64` | 0 | 6.37 |
| `avg_fare_usd` | `float64` | 0 | 50.0 |
| `weekly_frequency_est` | `int64` | 0 | 19 |
| `annual_revenue_usd_m` | `float64` | 0 | 320.5 |

---

#### `airline_route_profitability.csv`
- **Path:** `data/route_profitability/airline_route_profitability.csv`
- **Record Count:** 7,974 rows
- **Column Count:** 33 columns
- **Coverage:** 2024-01-01 to 2024-12-31

| Attribute Name | Data Type | Null Count | Sample Value |
| :--- | :--- | :---: | :--- |
| `Flight_Number` | `object` | 0 | EK8960 |
| `Flight_Date` | `object` | 0 | 2024-12-20 |
| `Origin` | `object` | 0 | DXB |
| `Destination` | `object` | 0 | ORD |
| `Route` | `object` | 0 | DXB-ORD |
| `Aircraft_Type` | `object` | 0 | Boeing 777-300ER |
| `Aircraft_Capacity` | `int64` | 0 | 396 |
| `Passengers` | `int64` | 0 | 308 |
| `Load_Factor` | `float64` | 0 | 0.7791 |
| `Flight_Hours` | `float64` | 0 | 14.5 |
| `Season` | `object` | 0 | Peak |
| `Route_Category` | `object` | 0 | Long Haul |
| `Demand_Level` | `object` | 0 | Medium |
| `Ticket_Revenue` | `float64` | 0 | 410785.49 |
| `Ancillary_Revenue` | `float64` | 271 | 53431.94 |
| *... and 18 more attributes* | | | |

---

