import requests

data = {
    'Age': 25.0, 
    'Gender': 1, 
    'Blood_Glucose_Reading': 90.0,
    'Diastolic_Blood_Pressure': 80.0, 
    'Systolic_Blood_Pressure': 120.0,
    'Heart_Rate': 75.0, 
    'Body_Temperature': 98.6, 
    'SPO2': 97.0,
    'Sweating_Y_N': 0.0, 
    'Shivering_Y_N': 0.0, 
    'Diastolic_Blood_Pressure_Level_High': 0.0,
    'Interaction_Glucose_HeartRate': 6750.0
}

response = requests.post('http://127.0.0.1:8000/predict', json=data)
print(response.json())