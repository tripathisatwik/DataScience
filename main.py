import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import os

#loading models 
try:
    with open('model_dt.pkl', 'rb') as f:
        model_dt = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        ss = pickle.load(f)
    with open('normalizer.pkl', 'rb') as f:
        norm = pickle.load(f)
    print("Model and preprocessors loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading pickle file: {e}. Make sure 'model_dt.pkl', 'scaler.pkl', and 'normalizer.pkl' are in the same directory as 'main.py'.")


#data model
class PredictionInput(BaseModel):
    Age: float
    Gender: int
    Blood_Glucose_Reading: float
    Diastolic_Blood_Pressure: float
    Systolic_Blood_Pressure: float
    Heart_Rate: float
    Body_Temperature: float
    SPO2: float
    Sweating_Y_N: float 
    Shivering_Y_N: float 
    Diastolic_Blood_Pressure_Level_High: float 
    Interaction_Glucose_HeartRate: float

app = FastAPI()

FEATURE_ORDER = [
    'Age',
    'Gender',
    'Blood Glucose Reading',
    'Diastolic Blood Pressure',
    'Systolic Blood Pressure',
    'Heart Rate',
    'Body Temperature',
    'SPO2',
    'Sweating  (Y/N)',
    'Shivering (Y/N)',
    'Diastolic Blood Pressure Level_High',
    'Interaction_Glucose_HeartRate'
]

PYDANTIC_TO_DF_COL_MAP = {
    "Age": "Age",
    "Gender": "Gender",
    "Blood_Glucose_Reading": "Blood Glucose Reading",
    "Diastolic_Blood_Pressure": "Diastolic Blood Pressure",
    "Systolic_Blood_Pressure": "Systolic Blood Pressure",
    "Heart_Rate": "Heart Rate",
    "Body_Temperature": "Body Temperature",
    "SPO2": "SPO2",
    "Sweating_Y_N": "Sweating  (Y/N)",
    "Shivering_Y_N": "Shivering (Y/N)",
    "Diastolic_Blood_Pressure_Level_High": "Diastolic Blood Pressure Level_High",
    "Interaction_Glucose_HeartRate": "Interaction_Glucose_HeartRate"
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Diabetes Prediction API"}

@app.post("/predict")
def predict_diabetes(data: PredictionInput):
    input_dict = data.model_dump()
    
    renamed_input_dict = {PYDANTIC_TO_DF_COL_MAP[key]: value for key, value in input_dict.items()}

    input_df = pd.DataFrame([renamed_input_dict])

    input_df = input_df[FEATURE_ORDER]

    scaled_data = ss.transform(input_df)
    normalized_data = norm.transform(scaled_data)

    prediction = model_dt.predict(normalized_data).tolist()
    return {"prediction": prediction[0]}