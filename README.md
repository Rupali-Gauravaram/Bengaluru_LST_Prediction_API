# Bengaluru_LST_Prediction_API

This repository showcases an **end-to-end MLOps pipeline** project, demonstrating the full cycle of creating a predictive product. The goal is to predict Land Surface Temperature (LST) based on Land Use/Land Cover across 198 BBMP wards in Bengaluru. The workflow covers:

* **Data Engineering:** Geospatial data wrangling and feature extraction (Built-up % and Green Cover%).
* **Model Creation:** Linear Regression training and validation (Mean Absolute Error, Root Mean Square Error).
* **Model Deployment:** Creating a ready-to-use API for real-time LST prediction.

## 1. Setup
The entire project is run in two distinct phases: Model Training (in the notebook) and API Deployment (using a Python script).

1.  **Clone the Repository**
    Use your specific repository link to download the project:
    ```bash
    git clone [https://github.com/Rupali-Gauravaram/Bengaluru_LST_Prediction_API.git](https://github.com/Rupali-Gauravaram/Bengaluru_LST_Prediction_API.git)
    cd Bengaluru_LST_Prediction_API
    ```

2.  **Install Dependencies**
    Install all required packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Model Training and Saving

The analysis notebook must be run first to train the model, evaluate performance, and generate the necessary deployment artifacts (joblib files) in the model/ folder. For immediate API testing, however, these artifacts are pre-committed to the repository for user convenience.

1.  **Run the Notebook**
    Open **`Bengaluru LST Prediction API.ipynb`** (or use your exact file name) and execute **all cells.**
    The final cells automatically save the trained model as `model/lst_model.joblib` and the feature names as `model/Xcolumn_names.joblib`.

## 3. API Deployment and Testing

Once the model files are saved, you can launch the prediction service. Note the built-in error handling in `LST_predictor.py` ensures the server will not start if the model files are missing.

1.  **Start the API Server**
    Open a terminal window in the project directory and run:
    ```bash
    python LST_predictor.py
    ```
    The server will start at: **`http://127.0.0.1:5000`**

2.  **Test the Prediction**
    Use Postman or cURL in a **new terminal** to send a POST request to the API.

    **Endpoint:** `http://127.0.0.1:5000/predict_lst`

    **cURL Command Example:**
    ```bash
    curl -X POST \
      -H "Content-Type: application/json" \
      -d '{"builtup_pct": 60.0, "green_pct": 20.0}' \
      [http://127.0.0.1:5000/predict_lst](http://127.0.0.1:5000/predict_lst)
    ```

    **Expected Result:** A JSON response with the predicted temperature (e.g., `{"predicted_mean_lst_c": 30.6387}`).

3.  **Stop:** Press `CTRL + C` in the terminal where the server is running.

---

## 4. Further Reading and Strategic Context

The technical work in this repository is part of a larger mission to drive data-informed sustainable design. To know more follow the links below:

* **Part 1: The Technical Deep Dive** - *[[Blog Post link](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-1/)]*
* **Part 2: The Strategic Vision** - *[[Blog Post link](https://chaiandcode.wordpress.com/2025/12/12/bengaluru-lst-prediction-api-part-2/)]*
