# Bengaluru Land Surface Temperature Prediction API

**An end-to-end machine learning pipeline predicting ward-level mean Land Surface Temperature across 198 BBMP wards of Bengaluru from satellite-derived land-use composition features. The model is trained in scikit-learn and served as a Flask REST API, providing the foundational predictive component on which subsequent supervised and unsupervised analyses are built.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-orange.svg) ![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey.svg)

---

## Motivation

Ward-level estimates of Land Surface Temperature (LST) for Bengaluru are typically obtained either by direct extraction from satellite imagery — a computationally and procedurally expensive process requiring repeated invocations of remote-sensing platforms — or from one-off academic studies whose outputs are not available through a programmatic interface. Neither option supports the latency and reproducibility requirements of an applied climate-intelligence tool.

This repository develops a parsimonious supervised model that returns a predicted mean LST in response to a small number of inputs describing the land-use composition of a candidate ward. The model is deployed behind a Flask REST API, making LST estimates available as a programmatic call rather than as the result of a manual extraction. The deployment is the principal contribution of this repository; the analytical extensions are developed in two companion repositories cross-referenced below.

---

## Data

The target variable is the long-term mean Land Surface Temperature in Celsius per BBMP ward, derived from the **MODIS/061/MOD11A2** 8-day composite product at 1 km spatial resolution. Values were extracted across the three-year window 2022–2024 to smooth seasonal variability, scaled by the MODIS conversion factor of 0.02, converted from Kelvin to Celsius, and aggregated to ward geometry via `ee.Reducer.mean()` in Google Earth Engine.

The predictor variables are built-up percentage and green-cover percentage per ward, derived from Sentinel-2 land-classification products and aggregated to the same ward geometry. The resulting dataset comprises 198 records with no missing values.

---

## Method

A **linear regression** model was fitted with the two ward-level land-use features as predictors and mean LST as the target. The model was implemented in scikit-learn and serialised to `joblib` artefacts for deployment. The fitted model and the feature-name ordering are loaded once at API startup and held in memory for inference.

The choice of a linear model with a restricted feature set was deliberate. Higher-capacity alternatives such as gradient-boosted ensembles would likely yield marginally lower error but would forfeit the directional interpretability of individual coefficients — a property that is itself a primary output of the analysis when reported in a planning context.

The API surface consists of a single POST endpoint, `/predict_lst`, accepting a JSON payload of two numeric fields and returning a predicted LST as a JSON response. Input validation and model-file availability checks are performed at startup, with the service refusing to start if the serialised artefacts are absent.

---

## Results

| Item | Value |
|---|---|
| Algorithm | Linear Regression (scikit-learn) |
| Features | `BuiltUp_Pct`, `Green_Pct` |
| Target | `Mean_LST_C` (long-term mean LST in °C, 2022–2024) |
| Mean Absolute Error | 0.39 °C |
| Root Mean Squared Error | 0.48 °C |
| Granularity | 198 BBMP wards |
| Spatial resolution | 1 km (MODIS MOD11A2) |
| Deployment | Flask REST API (port 5000) |

The reported MAE of 0.39 °C indicates that, on the held-out test set, the model's mean ward-level prediction deviates from the satellite-derived mean by approximately four-tenths of a degree Celsius. In the context of inter-ward LST variation (a range of roughly 5 °C across the 198 wards), this error is small relative to the signal and is suitable for ward-level planning and prioritisation tasks.

Full diagnostic plots — correlation heatmap, residual analysis, and predicted-versus-actual scatter — are reported in the companion repository [bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction), which extends this work with explicit downstream prioritisation logic.

---

## Discussion

### Positioning within a broader research programme

This repository is the foundational component of a three-repository sequence on Bengaluru ward-level climate analysis. The present work develops the prediction model and exposes it as a deployable service. The [bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction) repository extends the model with diagnostic validation, coefficient interpretation, and a downstream cool-roof prioritisation procedure. The [bengaluru-ward-climate-clustering](https://github.com/Rupali-Gauravaram/bengaluru-ward-climate-clustering) repository applies unsupervised K-Means partitioning to a four-feature variant of the dataset and produces a typology of ward archetypes that, independently, surfaces the same high-vulnerability wards identified by the supervised prioritisation. The convergence of the two methodologically distinct analyses on a common intervention set is established formally in the discussion section of each downstream repository.

### Deployment as the principal contribution

A predictive model whose outputs require manual extraction is, for applied purposes, equivalent to no model at all. The packaging of the trained regression as a callable REST endpoint — with deterministic model loading, explicit error handling on missing artefacts, and a stable JSON interface — is therefore not a secondary engineering concern but the principal value-add of this repository over a bare notebook. Subsequent work in the research programme assumes the model is available as a service and builds analytical layers above it.

---

## Limitations

- **Spatial resolution.** The 1 km MODIS resolution is appropriate for ward-level planning but cannot resolve sub-ward heterogeneity. Outputs should not be used for building-scale design decisions.
- **Land Surface Temperature versus ambient air temperature.** The target variable is LST, which is the appropriate metric for radiative balance and reflective-surface analysis but is not equivalent to ambient air temperature as experienced by residents.
- **Restricted feature scope.** The model uses two predictors. Inclusion of additional features (albedo, water-body proximity, elevation) would likely improve predictive accuracy at the cost of coefficient interpretability.
- **Static features.** Predictors are derived from long-term means and do not capture rapid changes in land-use composition.
- **Ward boundary set.** The analysis uses the 198-ward BBMP boundary set rather than the current 369-ward Greater Bengaluru Authority boundary. Re-extraction onto the GBA boundary is identified as the natural extension of this work.

---

## Reproducibility

The project runs in two phases: model training (in the notebook) and API deployment (via the Python script). The serialised model artefacts are pre-committed to the repository, so the API can be exercised without retraining.

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

Open `Bengaluru LST Prediction API.ipynb` and execute all cells. The final cells write the trained model to `model/lst_model.joblib` and the feature column order to `model/Xcolumn_names.joblib`.

### 4. Start the API

```bash
python LST_predictor.py
```

The service starts at `http://127.0.0.1:5000`. Startup will fail with an explicit message if the model artefacts are absent.

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

To stop the service, send `CTRL + C` in the terminal running it.

---

## Related work

- **[bengaluru-uhi-prediction](https://github.com/Rupali-Gauravaram/bengaluru-uhi-prediction)** — Extends this model with diagnostic validation, coefficient interpretation, and a downstream cool-roof prioritisation surfacing the ten wards most suited to thermal-retrofit intervention.
- **[bengaluru-ward-climate-clustering](https://github.com/Rupali-Gauravaram/bengaluru-ward-climate-clustering)** — Applies unsupervised K-Means to the same 198-ward dataset and produces a ward-typology that independently corroborates the supervised prioritisation.
- **Part 1: Technical Deep Dive** — [chaiandcode.wordpress.com](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-1/)
- **Part 2: Strategic Vision** — [chaiandcode.wordpress.com](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-2/)
- **[Bengaluru Quorum](https://linkedin.com/company/bengaluru-quorum)** — The climate-intelligence platform for which this prediction service provides foundational infrastructure.

---

## Author

**Rupali Gauravaram** — Climate Tech enthusiast, building [Bengaluru Quorum](https://linkedin.com/company/bengaluru-quorum). MSc Climate Resilience & Environmental Sustainability (University of Liverpool, 2024). Advanced AI/ML certification, IIT Roorkee (August, 2026).

[LinkedIn](https://linkedin.com/in/rupali99) · [GitHub](https://github.com/Rupali-Gauravaram) · [Blog: Chai & Code](https://chaiandcode.wordpress.com)
