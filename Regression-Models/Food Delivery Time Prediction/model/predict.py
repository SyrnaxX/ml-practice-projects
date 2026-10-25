import joblib
import pandas as pd
from pathlib import Path
# import model
MODEL_VERSION = '1.0.0'
model = joblib.load(Path(__file__).parent/'xgb_model.pkl')
def predict_output(user_input : dict):
    df = pd.DataFrame(user_input)
    prediction = model.predict(df)[0]
    return prediction