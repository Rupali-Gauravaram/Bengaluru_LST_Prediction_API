# Dataset 1: Land Surface Temperature (LST) Metrics 
**Description:**  
This dataset contains the calculated long-term mean Land Surface Temperature (LST) in Celsius for the 198 BBMP Wards.  
It serves as the **dependent variable (y)** for the Land Surface Temperature (LST) prediction model.

## 1. Data Source & Extraction Summary

The LST data was extracted using a **Geospatial Machine Learning (GeoML)** workflow implemented in **Google Earth Engine (GEE)**.
- **Time Period:**  
  - Jan 1, 2022 – Dec 31, 2024  

## 2. Key Columns

| Column Name     | Data Type | Description |
|-----------------|-----------|-------------|
| **Mean_LST_C**  | Float     | Mean Land Surface Temperature (°C) for the ward, averaged across 2022–2024 |


---

# Dataset 2: Land Use/Land Cover (LULC) Metrics
**Description:**  
This dataset contains the Land Use/Land Cover (LULC) metrics for the BBMP Wards.  
These percentages (**BuiltUp_Pct** and **Green_Pct**) are the **independent variables (X)** used to predict LST.

## 1. Data Source & Extraction Summary

The LULC metrics were generated using a high-precision **GeoML** workflow in **Google Earth Engine (GEE)**.  
- **Classification:**  
  - **Built-up Area**  
  - **Green Cover**

## 2. Key Columns

| Column Name        | Data Type | Description |
|--------------------|-----------|-------------|
| **BuiltUp_Pct**    | Float     | Percentage of land classified as Built-up within the ward |
| **Green_Pct**      | Float     | Percentage of land classified as Green Cover (Trees, Shrubland, Grassland) |
| **Total_Area_SqKm**| Float     | Total area of the ward in square kilometers |

