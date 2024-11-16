import os
import joblib
import pandas as pd

# Nạp mô hình từ file .joblib
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, 'model_file.joblib')
scaler_path = os.path.join(base_dir, 'scaler_file.joblib')
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

real_result = ['normal', 'abnormal']

def predict_health_status(age, weight, height, sex, bmi, temp, hr, spo2):
    true_sex = 0
    if true_sex == 'Male':
        true_sex = 1
    input_data = pd.DataFrame([[age, weight, height, true_sex, bmi, temp, hr, spo2]],
                              columns=['Age', 'Weight', 'Height', 'Sex', 'BMI', 'Temperature', 'Heart_rate', 'SPO2'])
    input_data_scaled = scaler.transform(input_data)
    result = model.predict(input_data_scaled)
    return real_result[result[0]]
