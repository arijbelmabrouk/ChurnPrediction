# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Production Churn API")

# Load the ONE source of truth
MODEL_PATH = "models/churn_pipeline.joblib"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Run the notebook to generate churn_pipeline.joblib first.")

model = joblib.load(MODEL_PATH)

# We use a flexible Pydantic model to avoid hardcoding every field twice
class ChurnRequest(BaseModel):
    data: dict 

@app.post("/predict")
async def predict(request: ChurnRequest):
    try:
        # Convert to DataFrame (The pipeline handles all string cleaning)
        input_df = pd.DataFrame([request.data])
        
        # Inference
        prob = model.predict_proba(input_df)[0][1]
        label = int(prob > 0.5)
        
        return {
            "churn_prediction": label,
            "probability": round(float(prob), 4),
            "engine": "Convex-Optimization-SAGA"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
