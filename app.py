import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
import pickle
import sqlite3

# Create flask app
flask_app = Flask(__name__, static_folder='assets')
flask_app.secret_key = 'your_secret_key'

# Try loading the model and scaler
try:
    model = pickle.load(open("model8feature.pkl", "rb"))
    sc = pickle.load(open("scaler.pkl", "rb"))  # Assuming the scaler is saved as scaler.pkl
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    model = None
    sc = None

# Database connection function to retrieve crop data
def get_crop_data():
    connection = sqlite3.connect("cropsList.db")  # Make sure your database is in the same directory or adjust path
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM crops")  # Fetch all crops from the database
    crops = cursor.fetchall()
    connection.close()
    return crops

# About Us
@flask_app.route("/")
def Home():
    return render_template("aboutus.html")

# Input form to collect data for prediction
@flask_app.route("/inputform", methods=['GET', 'POST'])
def inputform():
    if request.method == 'POST':
        # Capture the form data (soil and weather conditions)
        nitrogen = float(request.form['NitrogenInp'])
        potassium = float(request.form['PotassiumInp'])
        phosphorus = float(request.form['PhosphorusInp'])
        temperature = float(request.form['TemperatureInp'])
        rainfall = float(request.form['RainfallInp'])
        humidity = float(request.form['HumidityInp'])
        ph = float(request.form['PhInp'])

        # Prepare the input data
        feature_names = ["N", "P", "K", "temperature", "humidity", "ph","rainfall"]
        input_data = pd.DataFrame([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]], columns=feature_names)

        # Apply feature scaling using the loaded scaler (if available)
        if sc:
            input_data_scaled = sc.transform(input_data)  # Apply scaling

        # Make predictions if the model is loaded
        if model:
            probas = model.predict_proba(input_data_scaled)  # Get probabilities for each class
            top_5_indices = np.argsort(probas[0])[-5:][::-1]  # Get indices of the top 5 predictions
            top_5_crops = [model.classes_[i] for i in top_5_indices]  # Get the corresponding crop names
        else:
            top_5_crops = ["Maize", "Mungbeans", "Rice", "Coconut", "Mango"]  # Example crops for testing

        # Store the predictions in the session
        session['top_5_crops'] = top_5_crops

        # Retrieve crop details from the database
        crops = get_crop_data()
        top_crops_info = []
        if top_5_crops:
            # Assuming crops is a list of tuples with the format (id, name, explanation, trivia, image_filename)
            for crop_name in top_5_crops:
                for crop in crops:
                    if crop[1].lower() == crop_name.lower():  # Match crop names (case insensitive)
                        top_crops_info.append({
                            'name': crop_name,
                            'explanation': crop[2],
                            'trivia': crop[3],
                            'image': crop[4]
                        })

        # If no crop information found, set default info
        # if not top_crops_info:
        #     top_crops_info = [{'name': '1', 'explanation': '1', 'trivia': '1', 'image': "1"},
        #                       {'name': '2', 'explanation': '2', 'trivia': '2', 'image': "2"},
        #                       {'name': '3', 'explanation': '3', 'trivia': '3', 'image': "3"},
        #                       {'name': '4', 'explanation': '4', 'trivia': '4', 'image': "4"},
        #                       {'name': '5', 'explanation': '5', 'trivia': '5', 'image': "5"}]
        
        while len(top_crops_info) < 5:
            top_crops_info.append({
                'name': 'Default Crop',
                'explanation': 'Default Explanation',
                'trivia': 'Default Trivia',
                'image': 'default_image.jpg'})


        # Store the crop info in the session
        session['top_crops_info'] = top_crops_info

        return render_template("cropguide.html", predictions=top_crops_info)

    return render_template("inputform.html")

# Crop Guide page
@flask_app.route("/cropguide")
def cropguide():
    # Retrieve crop data from the database
    crops = get_crop_data()

    # Check if top 5 crops are available from the session
    top_5_crops = session.get('top_5_crops', None)
    top_crops_info = session.get('top_crops_info', None)

    if top_5_crops:
        # Display the crop information
        top_crops_info = []
        for crop_name in top_5_crops:
            for crop in crops:
                if crop[1].lower() == crop_name.lower():  # Match crop names (case insensitive)
                    top_crops_info.append({
                        'name': crop_name,
                        'explanation': crop[2],
                        'trivia': crop[3],
                        'image': crop[4]
                    })

        return render_template("cropguide.html", predictions=top_crops_info)
    else:
        # If no predictions, render the page with a message
        return render_template("cropguide.html", message="No predictions available. Please submit the form first.")

# Soil Optimization page
@flask_app.route("/soiloptimization")
def soiloptimization():
    return render_template("soiloptimization.html")

# Start the app
if __name__ == "__main__":
    flask_app.run(debug=True)
