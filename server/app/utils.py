import json
import pickle
import numpy as np
import pandas as pd
import os

__model = None
__locations = None
__data_columns = None


def load_artifacts():
    global __data_columns
    global __locations
    global __model
    
    # Get the absolute path to the artifacts directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(current_dir, "artifacts")
    
    # Load columns.json
    columns_path = os.path.join(artifacts_dir, "columns.json")
    with open(columns_path, 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    # Load model pickle file
    model_path = os.path.join(artifacts_dir, "banglore_home_prices_model.pickle")
    with open(model_path, 'rb') as f:
        __model = pickle.load(f)


def get_location_names():
    return __locations


def price_predict(location, sqft, bath, bhk):
    loc_index = -1

    if __data_columns is not None:
        loc_index = __data_columns.index(location.lower())
       
    else:
        raise ValueError("Error: __data_columns is None.")

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1


    if __model is not None:
        try:
            prediction = __model.predict([x])[0]
            return prediction
        except Exception as e:
            print(f"Prediction failed: {e}")
    else:
        raise ValueError("Model is not loaded.")


if __name__ == "__main__":
    print(__locations)
    load_artifacts()
    print(price_predict('1st block jayanagar',1000.3,1,3))
