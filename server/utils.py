import json
import pickle
import numpy as np
import pandas as pd

__model = None
__locations = None
__data_columns = None


def load_artifacts():
    global __data_columns
    global __locations
    global __model
    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open("./artifacts/banglore_home_prices_model.pickle", 'rb') as f:
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
    load_artifacts()
    print(price_predict('1st block jayanagar',1000.3,1,3))
