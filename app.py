# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:58:52 2022

@author: Admin
"""
from flask import Flask,render_template,request
import jsonify
import requests
import pickle
from datetime import date
import warnings
warnings.filterwarnings("ignore")
from flask import (url_for, current_app as app)
today = date.today().year  


app=Flask(__name__)
model = pickle.load(open("car_selling_price_regressor_model.pkl",'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

# favicon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='/images/my_favicon.png')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':    
        year= int(request.form['Year'])
        year= today - year
        present_price= float(request.form["Showroom_price"])
        kms= int(request.form['Kilometers'])
        owner= int(request.form['owners'])
        fuel_type = request.form['fuel_type']
        fuel_type_petrol = 0
        fuel_type_diesel = 0
        if fuel_type == 'petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        elif fuel_type_petrol == 'diesel':
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        else:
            pass
        seller_type = request.form['seller_type']
        seller_type_individual=0
        if seller_type == 'individual':
            seller_type_individual = 1
        transmission_type_manual=0
        transmission_type= request.form['transmission_type']
        if transmission_type == 'manual':
            transmission_type_manual = 1
        prediction=model.predict([[year,present_price,kms, owner, fuel_type_diesel ,fuel_type_petrol,seller_type_individual,transmission_type_manual]])
        prediction=round(prediction[0],2)
        return render_template('index.html',text=prediction)
    else:
        return render_template('index.html')
    
    
if (__name__ == "__main__"):
    app.run(debug=True)