from flask import Flask, request, jsonify
from flask_cors import CORS
import json 
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

__locations = None
__data_columns = None
__model = None


# Routines:
# Home:
@app.route('/')
def index():
    return "<h1>Bengaluru House Price Prediction API serving..</h1>"
# Locations fetcher:
@app.route('/locations', methods=['GET'])
def locations():
    load_saved_artifacts()
    response = jsonify({
        'locations': get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Predictor
@app.route('/predict_price', methods=['GET', 'POST'])
def predict_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



# Functions:
def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

def get_estimated_price(location,sqft,bhk,bath):
    try:
        load_saved_artifacts()
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = bhk
    x[2] = sqft
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/bengaluru_home_price_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")



if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()
    app.run(debug=True)