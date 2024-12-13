import sqlite3
import numpy as np
from flask import Flask, request, jsonify, render_template, session
import pickle

connection = sqlite3.connect("cropsList.db")  # Make sure your database is in the same directory or adjust path
cursor = connection.cursor()
cursor.execute("SELECT * FROM crops")  # Fetch all crops from the database
crops = cursor.fetchall()
connection.close()
    
print(crops[1][1])



try:
    model = pickle.load(open("modeltry.pkl", "rb"))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

while True:
    inp1=float(input("inp1: "))
    inp2=float(input("inp2: "))
    inp3=float(input("inp3: "))
    if inp1=="0":
        exit()
    input_data = np.array([[inp1, inp2, inp3]])
    if model:
        predictions = model.predict(input_data)  # Assuming your model can handle this input
        top_5_crops = predictions[:5]  # Adjust this based on your model's output format
    else:
        top_5_crops = ["Maize", "Mungbeans", "Rice", "Coconut", "Mango"] 
    print(top_5_crops)

