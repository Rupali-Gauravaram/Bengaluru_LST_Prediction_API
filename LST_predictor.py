from flask import Flask, request, jsonify
import joblib 
import pandas as pd
import sys 

# 1. CONFIGURATION AND LOADING THE MODEL
MODEL_FILENAME = 'model/lst_model.joblib'
COLUMNS_FILENAME = 'model/Xcolumn_names.joblib' 

# Load the Model and Feature Columns once when the app starts
try:
    MODEL = joblib.load(MODEL_FILENAME)
    FEATURE_COLUMNS = joblib.load(COLUMNS_FILENAME) 
    print(f"SUCCESS: Model and {len(FEATURE_COLUMNS)} features loaded from the 'model/' directory.")
except FileNotFoundError:
    print(f"ERROR: Could not find model files ({MODEL_FILENAME} or {COLUMNS_FILENAME}).")
    print("Please ensure the UHI_Bengaluru.ipynb notebook has been run completely.")
    sys.exit(1)
    
# 2. FLASK APPLICATION SETUP
app = Flask(__name__)

# Define the API endpoint that listens for POST requests
@app.route('/predict_lst', methods=['POST'])
def handle_prediction():
    data = request.get_json()
    
    # Simple extraction (error handling removed for simplicity)
    builtup = data['builtup_pct']
    green = data['green_pct']
    
    # Structure the input data using the loaded feature column names
    input_data = pd.DataFrame([[builtup, green]], columns=FEATURE_COLUMNS)
    
    # Get the prediction
    predicted_lst = MODEL.predict(input_data)[0]
    
    # Return the result
    return jsonify({
        'predicted_mean_lst_c': round(float(predicted_lst), 4)
    })

# 3. RUN THE API
if __name__ == '__main__':
    print("\n--- LST Prediction Service Initialized ---")
    app.run(debug=True, port=5000)