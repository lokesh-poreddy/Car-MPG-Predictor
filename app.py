from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

app = Flask(__name__)

# Load the dataset
try:
    print("Loading dataset...")
    df = pd.read_csv('../auto_mpg.csv')
    # Convert horsepower to numeric, handling any '?' values
    df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
    # Drop any rows with missing values
    df = df.dropna()
    print("Dataset loaded successfully")
    
    # Train and save model immediately
    features = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year']
    X = df[features]
    y = df['mpg']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Save the model
    joblib.dump(model, 'models/car_model.pkl')
    print("Model trained and saved successfully")
    
except Exception as e:
    print(f"Error: {str(e)}")

@app.route('/')
def home():
    print("Accessing home route")
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year']
        input_data = [float(data[feature]) for feature in features]
        
        # Train model if not exists
        if not os.path.exists('models/car_model.pkl'):
            X = df[features]
            y = df['mpg']
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            joblib.dump(model, 'models/car_model.pkl')
        else:
            model = joblib.load('models/car_model.pkl')
            
        prediction = model.predict([input_data])
        return jsonify({'success': True, 'prediction': float(prediction[0])})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True)