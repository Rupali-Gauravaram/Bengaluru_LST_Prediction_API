# Bengaluru_LST_Prediction_API
This repository showcases an end-to-end MLOps workflow, covering data engineering (wrangling, feature extraction), model creation (Linear Regression) with model metrics evaluation (Mean Absolute Error, Root Mean Square Error), and finally, API deployment for real-time Land Surface Temperature (LST) prediction based on Urban Heat Island (UHI) factors.

## 1. Setup

The entire project is run in two distinct phases: Model Training (in the notebook) and API Deployment (using a Python script).

1.  **Clone the Repository**
    Use your specific repository link to download the project:
    ```bash
    git clone [https://github.com/Rupali-Gauravaram/Bengaluru_LST_Prediction_API.git](https://github.com/Rupali-Gauravaram/Bengaluru_LST_Prediction_API.git)
    cd Bengaluru_LST_Prediction_API
    ```

2.  **Install Dependencies**
    Install all required packages:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Model Training and Saving

You must run the analysis notebook first to train the model and generate the necessary deployment files in the `model/` folder.

1.  **Run the Notebook**
    Open **`UHI_Bengaluru.ipynb`** and execute **all cells.**
    The final cells automatically save the trained model as `model/lst_model.joblib` and the feature names as `model/Xcolumn_names.joblib`.

## 3. API Deployment and Testing

Once the model files are saved, you can launch the prediction service.

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
