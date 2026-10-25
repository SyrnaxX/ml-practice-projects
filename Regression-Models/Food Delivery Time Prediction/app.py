from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
import pandas as pd
from schema.user_input import userInput
from model.predict import predict_output,MODEL_VERSION,model
app = FastAPI()

@app.get('/')
def home():
    return {'message': 'This is Food Delivery Time Prediction API'}
@app.get('/health')
def get_health():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None,
    }
@app.get('/predict')
def predict():
    pass