# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os
# Import all custom transformers
from model_utils import *

app = FastAPI()

# Load individual model components
models_dir = "models"

try:
    print("Loading model components...")
    yes_no_encoder = joblib.load(os.path.join(models_dir, "yes_no_encoder.joblib"))
    label_encoder = joblib.load(os.path.join(models_dir, "label_encoder.joblib"))
    target_encoder = joblib.load(os.path.join(models_dir, "target_encoder.joblib"))
    log_transformer = joblib.load(os.path.join(models_dir, "log_transformer.joblib"))
    boxcox_transformer = joblib.load(os.path.join(models_dir, "boxcox_transformer.joblib"))
    column_dropper = joblib.load(os.path.join(models_dir, "column_dropper.joblib"))
    standardizer = joblib.load(os.path.join(models_dir, "standardizer.joblib"))
    classifier = joblib.load(os.path.join(models_dir, "classifier.joblib"))
    
    # Load column configuration
    column_config = joblib.load(os.path.join(models_dir, "column_config.joblib"))
    print("All model components loaded successfully")
except Exception as e:
    print(f"Error loading model components: {str(e)}")
    raise RuntimeError("Failed to load model components. Please run train_model.py first.")

class CustomerData(BaseModel):
    Tenure_in_Months: int
    Offer: str
    Phone_Service: str
    Avg_Monthly_Long_Distance_Charges: float
    Multiple_Lines: str
    Internet_Type: str
    Avg_Monthly_GB_Download: float
    Online_Security: str
    Online_Backup: str
    Device_Protection_Plan: str
    Premium_Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Streaming_Music: str
    Unlimited_Data: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charge: float
    Total_Charges: float
    Total_Refunds: float
    Total_Extra_Data_Charges: float
    Total_Long_Distance_Charges: float
    Total_Revenue: float
    Satisfaction_Score: int
    CLTV: float
    Gender: str
    Age: int
    Under_30: str
    Senior_Citizen: str
    Married: str
    Dependents: str
    Number_of_Dependents: int

@app.post("/predict")
async def predict(data: CustomerData):
    try:
        # Convert Pydantic model to dict
        data_dict = data.dict()
        
        # Convert snake_case to space-separated format
        formatted_data = {}
        for key, value in data_dict.items():
            formatted_key = key.replace('_', ' ')
            formatted_data[formatted_key] = value
        
        # Create DataFrame from input data
        df = pd.DataFrame([formatted_data])
        
        # Apply transformations in sequence
        df = yes_no_encoder.transform(df)
        df = label_encoder.transform(df)
        df = target_encoder.transform(df)
        df = log_transformer.transform(df)
        df = boxcox_transformer.transform(df)
        df = column_dropper.transform(df)
        df = standardizer.transform(df)
        
        # Make prediction
        prediction = classifier.predict(df)[0]
        probabilities = classifier.predict_proba(df)[0]
        
        # Get probability of no churn (class 0) and churn (class 1)
        no_churn_probability = float(probabilities[0])
        churn_probability = float(probabilities[1])
        
        return {
            "churn_prediction": int(prediction),
            "no_churn_probability": no_churn_probability,
            "churn_probability": churn_probability,
            "message": "Prediction successful"
        }
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Churn prediction API is running"}