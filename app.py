import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__, static_folder='assets')

# Try loading the model
try:
    model = pickle.load(open("model.pkl", "rb"))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

#About us 
@flask_app.route("/")
def Home():
    return render_template("aboutus.html")

@flask_app.route("/inputform")
def inputform():
    return render_template("inputform.html")

@flask_app.route("/cropguide")
def cropguide():
    return render_template("cropguide.html")

@flask_app.route("/soiloptimization")
def soiloptimization():
    return render_template("soiloptimization.html")





































# @flask_app.route("/")
# def Home():
#     return render_template("form.html")

# @flask_app.route("/predict", methods=["POST"])
# def predict():
#     if model is None:
#         return render_template("index.html", error_message="Model not loaded properly.")

#     try:
#         # Ensure that the features are numeric
#         float_features = [float(x) for x in request.form.values()]
#     except ValueError:
#         return render_template("index.html", error_message="Please enter numeric values for temperature, humidity, and pH level.")
    
#     # Check if we have exactly 3 input features
#     if len(float_features) != 3:
#         return render_template("index.html", error_message="Please provide exactly 3 features: temperature, humidity, and pH level.")
    
#     features = [np.array(float_features)]
    
#     try:
#         prediction = model.predict(features)
#         predicted_crop = prediction[0].capitalize()
#         return render_template("index.html", prediction_text=predicted_crop)
#     except Exception as e:
#         return render_template("index.html", error_message=f"Prediction error: {str(e)}")

if __name__ == "__main__":
     flask_app.run(debug=True)
