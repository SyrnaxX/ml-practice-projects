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
# ---------------------Post---------------------------
@app.post('/predict')
def predict(data: userInput):
    user_input_dict = pd.DataFrame([{
        "Road_Distance_km" : data.Road_Distance_km,
        "Is_Weekend" : data.Is_Weekend,
        'Is_Festival': data.Is_Festival,
        'Weather' : data.Weather,
        'Pickup_Zone': data.Pickup_Zone,
        'Dropoff_Zone' : data.Dropoff_Zone,
        'Vehicle_Type' : data.Vehicle_Type,
        'Rider_Rating' : data.Rider_Rating,
        'Cuisine_Type' : data.Cuisine_Type,
        'Order_Items' : data.Order_Items,
        'Road_Distance_km' : data.Road_Distance_km,
        'Delivery_Distance_Category' : data.Delivery_Distance_Category,
        'Traffic_Level' : data.Traffic_Level,
        'Number_of_Signals' : data.No_of_signals,
        'Time_period' :  data.Time_period
    }])
    try:
        prediction = predict_output(user_input_dict)
        return JSONResponse(status_code=200,content= f"{prediction:.2f}")
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))