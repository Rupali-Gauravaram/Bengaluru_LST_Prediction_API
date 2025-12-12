# Dataset 1: Land Surface Temperature (LST) Metrics

**Filename:** `BBMP_Wards_LST_Metrics.csv`  
**Description:**  
This dataset contains the calculated long-term mean Land Surface Temperature (LST) in Celsius for the 198 BBMP Wards.  
It serves as the **dependent variable (y)** for the Urban Heat Island (UHI) prediction model.

## 1. Data Source & Extraction Summary

The LST data was extracted using a **Geospatial Machine Learning (GeoML)** workflow implemented in **Google Earth Engine (GEE)**.

- **Source:** MODIS/061/MOD11A2 (8-day composite)  
- **Time Period:**  
  - Jan 1, 2022 – Dec 31, 2024  
  - Three-year average ensures a stable, climatologically representative baseline, avoiding single-day anomalies
- **Processing:**  
  - Raw LST (1 km resolution) scaled and converted from Kelvin to Celsius  
  - Final **Mean LST** computed by spatially averaging values within each BBMP Ward boundary

## 2. Constraints and Limitations

| **Constraint**       | **Key Rationale** | **Impact on Project** |
|----------------------|-------------------|------------------------|
| **Data Resolution**  | LST is macro-level (~1 km resolution) | Suitable for city-scale planning, not façade-level micro-design |
| **Temporal Choice**  | 3-year averaging smooths variability | Model coefficients reflect stable LULC impacts instead of transient weather |
| **Temperature Type** | LST measures surface/roof temperature, not air temperature | LST is the correct metric for modeling UHI and thermal load |

## Key Column

| Column Name     | Data Type | Description |
|-----------------|-----------|-------------|
| **Mean_LST_C**  | Float     | Mean Land Surface Temperature (°C) for the ward, averaged across 2022–2024 |


---

# Dataset 2: Land Use/Land Cover (LULC) Metrics

**Filename:** `BBMP_Wards_LULC_Metrics.csv`  
**Description:**  
This dataset contains the Land Use/Land Cover (LULC) metrics for the BBMP Wards.  
These percentages (**BuiltUp_Pct** and **Green_Pct**) are the **independent variables (X)** used to predict LST.

## 1. Data Source & Extraction Summary

The LULC metrics were generated using a high-precision **GeoML** workflow in **Google Earth Engine (GEE)**.

- **Source:** ESA WorldCover 10m v100 (Sentinel-1 & Sentinel-2 based)  
- **Resolution:** High-resolution **10 m** data for precise class calculations  
- **Classification:**  
  - **Built-up Area:** WorldCover class ID **50**  
  - **Green Cover:** Combined area of **Trees (10)**, **Shrubland (20)**, **Grassland (30)**
- **Processing:**  
  - Area of each class calculated within ward boundaries  
  - Normalized to total ward area to compute final percentage metrics

## 2. Constraints and Limitations

| **Constraint**       | **Key Rationale** | **Impact on Project** |
|----------------------|-------------------|------------------------|
| **Data Resolution**  | High 10 m resolution enables accurate class delineation | Minimizes measurement error in Built-up and Green percentages |
| **Explanatory Goal** | Percent metrics used as regression inputs | Ensures API outputs are simple, interpretable, and actionable for design decisions |

## Key Columns

| Column Name        | Data Type | Description |
|--------------------|-----------|-------------|
| **BuiltUp_Pct**    | Float     | Percentage of land classified as Built-up within the ward |
| **Green_Pct**      | Float     | Percentage of land classified as Green Cover (Trees, Shrubland, Grassland) |
| **Total_Area_SqKm**| Float     | Total area of the ward in square kilometers |

