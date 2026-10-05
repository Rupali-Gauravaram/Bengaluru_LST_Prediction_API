# Bengaluru Land Surface Temperature Prediction API

**I built a machine learning model that predicts the average land surface temperature of a Bengaluru ward from two land-use features: how built-up it is and how green it is. The model covers 198 BBMP wards, is trained in scikit-learn, and is served as a Flask REST API. It is the starting point for two follow-up projects on the same data.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-orange.svg) ![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey.svg)

---

## Motivation

Getting ward-level Land Surface Temperature (LST) for Bengaluru usually means extracting it from satellite imagery each time, which is slow, or relying on one-off academic studies whose results cannot be queried by a program. Neither works well for a tool that needs quick, repeatable answers.

This project builds a small model that returns a predicted mean LST from two inputs describing a ward's land use. I put it behind a Flask REST API, so an estimate is one request away. The deployed API is the main point of this repository. The analysis is taken further in the two companion repositories listed below.

---

## Data

**Target:** the long-term mean Land Surface Temperature per BBMP ward, in Celsius. It comes from the **MODIS/061/MOD11A2** 8-day product at 1 km resolution. I used the three years 2022 to 2024 to smooth out seasonal changes, applied the MODIS scale factor of 0.02, converted from Kelvin to Celsius, and averaged over each ward's boundary with `ee.Reducer.mean()` in Google Earth Engine.

**Features:** built-up percentage and green-cover percentage per ward, from Sentinel-2 land-classification products, averaged over the same ward boundaries.

The final dataset has 198 rows and no missing values.

---

## Method

I fitted a **linear regression** with the two land-use features as inputs and mean LST as the target. The model is built in scikit-learn and saved with `joblib`. The API loads the model and the feature order once at startup and keeps them in memory.

I chose a simple linear model with two features on purpose. A more complex model, such as gradient boosting, might give a slightly lower error, but the coefficients would no longer be easy to read. For planning, being able to say how much each feature moves the temperature is itself a useful result.

The API has one POST endpoint, `/predict_lst`. It takes a JSON body with two numbers and returns the predicted LST as JSON. At startup the service checks that the model files exist, and refuses to start if they are missing.

---

## Results

| Item | Value |
|---|---|
| Algorithm | Linear Regression (scikit-learn) |
| Features | `BuiltUp_Pct`, `Green_Pct` |
| Target | `Mean_LST_C` (long-term mean LST in °C, 2022 to 2024) |
| Mean Absolute Error | 0.39 °C |
| Root Mean Squared Error | 0.48 °C |
| Granularity | 198 BBMP wards |
| Spatial resolution | 1 km (MODIS MOD11A2) |
| Deployment | Flask REST API (port 5000) |

An MAE of 0.39 °C means that, on the test set, the prediction is off by about four-tenths of a degree on average. The wards differ from each other by about 5 °C, so this error is small compared with the differences the model needs to capture. That makes it suitable for ward-level planning and prioritisation.

The diagnostic plots (correlation heatmap, residuals, predicted vs actual) are in the companion repository [bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction), which adds a prioritisation step on top of this model.

---

## How this fits with my other repositories

This is the first of three repositories on Bengaluru ward-level climate analysis:

1. **This repository** builds the prediction model and serves it as an API.
2. **[bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction)** adds diagnostics, reads the coefficients, and ranks wards for cool-roof work.
3. **[bengaluru-ward-climate-clustering](https://github.com/Rupali-Gauravaram/bengaluru-ward-climate-clustering)** groups the wards with K-Means using four features. Without using any labels, it points to the same high-risk wards as the ranking in repository 2.

Two different methods arriving at the same wards gives more confidence in the result.

**Why the API matters:** a model whose output has to be extracted by hand is not much use in practice. Serving it as an endpoint, with the model loaded once, clear errors when files are missing, and a stable JSON format, is what turns a notebook into something another tool can use.

---

## Limitations

- **Spatial resolution.** 1 km MODIS data suits ward-level planning but cannot show differences inside a ward. It should not be used for decisions about single buildings.
- **Surface temperature is not air temperature:** LST is the right measure for studying reflective surfaces, but it is not the air temperature people feel.
- **Only two features:** Adding albedo, distance to water, or elevation would probably improve accuracy, but the coefficients would be harder to interpret.
- **Static features:** The inputs are long-term averages, so they do not capture fast changes in land use.
- **Ward boundaries:** The analysis uses the 198-ward BBMP boundaries, not the current 369-ward Greater Bengaluru Authority boundaries. Re-extracting the data for the new boundaries is the natural next step.

---

## Reproduction

The project has two parts: training the model (in the notebook) and running the API (the Python script). The trained model files are already in the repository, so you can run the API without retraining.

### 1. Clone the repository

```bash
git clone https://github.com/Rupali-Gauravaram/Bengaluru_LST_Prediction_API.git
cd Bengaluru_LST_Prediction_API
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Retrain the model

Open `Bengaluru LST Prediction API.ipynb` and run all cells. The last cells save the trained model to `model/lst_model.joblib` and the feature order to `model/Xcolumn_names.joblib`.

### 4. Start the API

```bash
python LST_predictor.py
```
The service starts at `http://127.0.0.1:5000`. It stops with a clear message if the model files are missing.

### 5. Request a prediction

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"builtup_pct": 60.0, "green_pct": 20.0}' \
  http://127.0.0.1:5000/predict_lst
```

Expected response:
```json
{"predicted_mean_lst_c": 30.6387}
```
---

## Related work

- **[bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction)**: adds diagnostics, coefficient interpretation, and a cool-roof ranking of the ten wards that would benefit most.
- **[bengaluru-ward-climate-clustering](https://github.com/Rupali-Gauravaram/bengaluru-ward-climate-clustering)**: K-Means clustering of the same 198 wards, which independently supports the ranking.
- **Part 1: Technical Deep Dive**: [chaiandcode.wordpress.com](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-1/)
- **Part 2: Strategic Vision**: [chaiandcode.wordpress.com](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-2/)
- **[Bengaluru Quorum](https://linkedin.com/company/bengaluru-quorum)**: the climate-intelligence platform this prediction service was built for.

---

## Author

**Rupali Gauravaram**. MSc Climate Resilience & Environmental Sustainability (University of Liverpool, 2024). Advanced Certification in Data Science & AI (IIT Roorkee).

[LinkedIn](https://linkedin.com/in/rupali99) · [GitHub](https://github.com/Rupali-Gauravaram) · [Blog: Chai & Code](https://chaiandcode.wordpress.com)
