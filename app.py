import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, session, g, url_for
import pickle
import sqlite3
import json
from collections import OrderedDict
import csv

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
def get_crop_data():
    crop_data = []
    try:
        with open('crops_data.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                crop_data.append({
                    'name': row[0],
                    'explanation': row[1],
                    'trivia': row[2],
                    'image': row[3]
                })
    except FileNotFoundError:
        print("CSV file not found")
        return None
    return crop_data

crops = get_crop_data()


optimal_ranges =  {'rice': {'N': (60.0, 99.0), 'P': (35.0, 60.0), 'K': (35.0, 45.0), 'temperature': (20.0454142, 26.92995077), 'humidity': (80.12267476, 84.96907151), 'ph': (5.005306977, 7.868474653), 'rainfall': (182.5616319, 298.5601175)}, 'maize': {'N': (60.0, 100.0), 'P': (35.0, 60.0), 'K': (15.0, 25.0), 'temperature': (18.04185513, 26.54986394), 'humidity': (55.28220433, 74.82913698), 'ph': (5.513697923, 6.995843776), 'rainfall': (60.65171481, 109.7515385)}, 'chickpea': {'N': (20.0, 60.0), 'P': (55.0, 80.0), 'K': (75.0, 85.0), 'temperature': (17.02498456, 20.99502153), 'humidity': (14.25803981, 19.96978871), 'ph': (5.988992796000002, 8.868741443), 'rainfall': (65.11365631, 94.78189594)}, 'kidneybeans': {'N': (0.0, 40.0), 'P': (55.0, 80.0), 'K': (15.0, 25.0), 'temperature': (15.33042636, 24.92360104), 'humidity': (18.09224048, 24.96969858), 'ph': (5.502999119, 5.99812453), 'rainfall': (60.27552528, 149.7441028)}, 'pigeonpeas': {'N': (0.0, 40.0), 'P': (55.0, 80.0), 'K': (15.0, 25.0), 'temperature': (18.31910448, 36.97794384), 'humidity': (30.40046769, 69.69141302), 'ph': (4.548202098, 7.445444882999999), 'rainfall': (90.05422663, 198.8298806)}, 'mothbeans': {'N': (0.0, 40.0), 'P': (35.0, 60.0), 'K': (15.0, 25.0), 'temperature': (24.01825377, 31.99928579), 'humidity': (40.00933429, 64.95585424), 'ph': (3.504752314, 9.93509073), 'rainfall': (30.92014047, 74.44330654)}, 'mungbean': {'N': (0.0, 40.0), 'P': (35.0, 60.0), 'K': (15.0, 25.0), 'temperature': (27.01470397, 29.914544300000006), 'humidity': (80.03499648, 89.99615558), 'ph': (6.218923893, 7.199495367999999), 'rainfall': (36.12042927, 59.87232071)}, 'blackgram': {'N': (20.0, 60.0), 'P': (55.0, 80.0), 'K': (15.0, 25.0), 'temperature': (25.09737391, 34.9466155), 'humidity': (60.06534859, 69.96100028), 'ph': (6.500144962, 7.775306272000001), 'rainfall': (60.41790253, 74.91559514)}, 'lentil': {'N': (0.0, 40.0), 'P': (55.0, 80.0), 'K': (15.0, 25.0), 'temperature': (18.06486101, 29.94413861), 'humidity': (60.09116626, 69.92375891), 'ph': (5.91645379, 7.841496029), 'rainfall': (35.03484812, 54.93937710000001)}, 'pomegranate': {'N': (0.0, 40.0), 'P': (5.0, 30.0), 'K': (35.0, 45.0), 'temperature': (18.07132963, 24.96273236), 'humidity': (85.12912161, 94.99897537), 'ph': (5.561851831, 7.199504273), 'rainfall': (102.5184759, 112.4750941)}, 'banana': {'N': (80.0, 120.0), 'P': (70.0, 95.0), 'K': (45.0, 55.0), 'temperature': (25.01018457, 29.90888522), 'humidity': (75.03193255, 84.97849241), 'ph': (5.505393832999999, 6.490074429), 'rainfall': (90.10978128, 119.84797)}, 'mango': {'N': (0.0, 40.0), 'P': (15.0, 40.0), 'K': (25.0, 35.0), 'temperature': (27.00315545, 35.99009679), 'humidity': (45.02236377, 54.9640534), 'ph': (4.507523551, 6.9674177660000005), 'rainfall': (89.29147581, 100.8124659)}, 'grapes': {'N': (0.0, 40.0), 'P': (120.0, 145.0), 'K': (195.0, 205.0), 'temperature': (8.825674745, 41.94865736), 'humidity': (80.01639435, 83.98351748), 'ph': (5.510924848999999, 6.499604931), 'rainfall': (65.01095312, 74.91506217)}, 'watermelon': {'N': (80.0, 120.0), 'P': (5.0, 30.0), 'K': (45.0, 55.0), 'temperature': (24.04355803, 26.98603693), 'humidity': (80.02621335, 89.98405233), 'ph': (6.000975617000001, 6.956508826), 'rainfall': (40.12650421, 59.75980023)}, 'muskmelon': {'N': (80.0, 120.0), 'P': (5.0, 30.0), 'K': (45.0, 55.0), 'temperature': (27.02415146, 29.94349168), 'humidity': (90.01506395, 94.96218673), 'ph': (6.002927293, 6.781050372999999), 'rainfall': (20.21126747, 29.86681385)}, 'apple': {'N': (0.0, 40.0), 'P': (120.0, 145.0), 'K': (195.0, 205.0), 'temperature': (21.0365275, 23.99686172), 'humidity': (90.02575116, 94.92048112), 'ph': (5.514253142, 6.4992268210000015), 'rainfall': (100.1173443, 124.9831618)}, 'orange': {'N': (0.0, 40.0), 'P': (5.0, 30.0), 'K': (5.0, 15.0), 'temperature': (10.01081312, 34.90665289), 'humidity': (90.00621688, 94.96419851), 'ph': (6.010391864, 7.995848977), 'rainfall': (100.1737964, 119.6946577)}, 'papaya': {'N': (31.0, 70.0), 'P': (46.0, 70.0), 'K': (45.0, 55.0), 'temperature': (23.012401800000006, 43.67549305), 'humidity': (90.03863107, 94.94482086), 'ph': (6.501521192, 6.993473247000001), 'rainfall': (40.35153141, 248.8592986)}, 'coconut': {'N': (0.0, 40.0), 'P': (5.0, 30.0), 'K': (25.0, 35.0), 'temperature': (25.00872392, 29.8690834), 'humidity': (90.01734526, 99.98187601), 'ph': (5.50158009, 6.470465614), 'rainfall': (131.09000759999998, 225.6323656)}, 'cotton': {'N': (100.0, 140.0), 'P': (35.0, 60.0), 'K': (15.0, 25.0), 'temperature': (22.00085141, 25.99237426), 'humidity': (75.00539324, 84.87668973), 'ph': (5.801047545, 7.994679507000001), 'rainfall': (60.65381719, 99.93100821)}, 'jute': {'N': (60.0, 100.0), 'P': (35.0, 60.0), 'K': (35.0, 45.0), 'temperature': (23.09433785, 26.98582182), 'humidity': (70.88259632, 89.89106506), 'ph': (6.002524871, 7.4880144039999985), 'rainfall': (150.2355238, 199.83629130000003)}, 'coffee': {'N': (80.0, 120.0), 'P': (15.0, 40.0), 'K': (25.0, 35.0), 'temperature': (23.05951896, 27.92374437), 'humidity': (50.04557009, 69.94807345), 'ph': (6.020947179, 7.493191968), 'rainfall': (115.1564012, 199.4735636)}, 'bitter gourd': {'N': (50.27862694160192, 79.95377064656769), 'P': (30.261736395662457, 59.941531282126505), 'K': (40.04538041285054, 69.6965986726604), 'temperature': (25.146855116292567, 34.994802402366545), 'humidity': (70.00038660721052, 79.93827742281796), 'ph': (6.0018650556272695, 6.994905303133312), 'rainfall': (800.0742441312, 1198.6174770310045)}, 'kangkong': {'N': (40.03378622849257, 69.99175963524459), 'P': (20.35595805627552, 49.81664186062281), 'K': (30.23935366038159, 59.99750541466314), 'temperature': (25.06756371225477, 29.98812272856055), 'humidity': (80.03140327373391, 89.95362171874191), 'ph': (6.5004442849915325, 7.481111379576125), 'rainfall': (1200.8826358007543, 1498.7869776986408)}, 'string beans': {'N': (60.22511173054931, 89.99121366336747), 'P': (40.18392111886316, 69.90870673841295), 'K': (40.16407574093141, 79.98398184323098), 'temperature': (20.06065932348673, 29.89736827197164), 'humidity': (60.08575240219567, 79.82892341254811), 'ph': (6.011991944737577, 6.996675021688802), 'rainfall': (1000.5962860303644, 1493.4108108778437)}, 'pechay': {'N': (40.02157522182119, 59.9733887937372), 'P': (20.03613851753036, 39.93582115961658), 'K': (30.13757205794189, 49.99274792709272), 'temperature': (18.007426943214853, 24.993324908434666), 'humidity': (70.0060347453264, 79.96753302005857), 'ph': (6.005046441094226, 6.499915280170552), 'rainfall': (800.1953576152728, 1198.6872928002426)}, 'okra': {'N': (50.27458152421983, 69.8800228251351), 'P': (30.30829624343181, 49.92616100575209), 'K': (40.18058581219171, 69.5827826194874), 'temperature': (25.02427065669189, 34.973724818345545), 'humidity': (60.06107270184379, 79.89777743662918), 'ph': (6.503370817784264, 7.49658113455232), 'rainfall': (702.6044191238454, 999.8092566696076)}}

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
        session['input_data'] = OrderedDict(input_data.to_dict(orient='records')[0]) # Use OrderedDict
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
        if top_5_crops and crops:  # Check if both lists are not None
            for crop_name in top_5_crops:
                for crop in crops:
                    if crop['name'].lower() == crop_name.lower():  # Use dictionary key 'name'
                        top_crops_info.append({
                            'name': crop_name,
                            'explanation': crop['explanation'],  # Use dictionary key 'explanation'
                            'trivia': crop['trivia'],        # Use dictionary key 'trivia'
                            'image': crop['image']         # Use dictionary key 'image'
                        })
  
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
    
    top_crops_info = session.get('top_crops_info', None)


    return render_template("cropguide.html", predictions=top_crops_info, )

@flask_app.route("/soiloptimization", methods=['GET', 'POST'])
def soiloptimization():
    crops = get_crop_data()
    selected_crop = request.form.get('crop')

    user_data = session.get('input_data')
    feedback = {}
    if request.method == 'POST':
        if user_data:
            feature_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            optimal_range = optimal_ranges.get(selected_crop.lower())
            if optimal_range:
                for feature in feature_names:
                    if feature in optimal_range:
                        value = user_data.get(feature)
                        min_val, max_val = optimal_range[feature]

                        # Add units to the feedback messages
                        unit = ""
                        if feature == "temperature":
                            unit = " °C"
                        elif feature == "humidity":
                            unit = " %"
                        elif feature == "rainfall":
                            unit = " mm"
                        elif feature in ["N", "P", "K"]:
                            unit = " (ratio content in soil)"

                        if value < min_val:
                            feedback[feature] = f"Needs improvement (increase value). Optimal range: {round(min_val)}{unit}-{round(max_val)}{unit}"
                        elif value > max_val:
                            feedback[feature] = f"May be harmful (reduce value). Optimal range: {round(min_val)}{unit}-{round(max_val)}{unit}"
                        else:
                            feedback[feature] = f"Good. Optimal range: {round(min_val)}{unit}-{round(max_val)}{unit}"
                    else:
                        feedback[feature] = "Optimal range data not available for this feature."
            else:
                feedback["crop"] = f"Optimal range data not available for {selected_crop}."
        else:
            if not selected_crop:
                feedback["crop_selection"] = "Please select a crop."
            if not user_data:
                feedback["input_data"] = "Please submit input form first."
    return render_template("soiloptimization.html", crops=crops, feedback=feedback, selected_crop=selected_crop, user_data=user_data)


# Start the app
if __name__ == "__main__":
    flask_app.run(debug=True)
