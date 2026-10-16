import streamlit as st
import pandas as pd
import joblib
import os

# 1. Basic Page Setup
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# 2. Load Data and Model
@st.cache_data
def load_data():
    return pd.read_csv('Cleaned car data.csv')

@st.cache_resource
def load_model():
    # Make sure this filename matches your saved model exactly!
    return joblib.load('car_price_dt_model.pkl')

data = load_data()
model = load_model()

# 3. Simple UI Layout
st.title("🚗 Used Car Price Predictor")
st.write("Enter the details below to get an estimated selling price.")
st.markdown("---")

# Inputs arranged in columns
col1, col2 = st.columns(2)

with col1:
    name = st.selectbox("Car Name / Brand", sorted(data['name'].unique()))
    fuel = st.selectbox("Fuel Type", sorted(data['fuel'].unique()))
    transmission = st.selectbox("Transmission", sorted(data['transmission'].unique()))
    owner = st.selectbox("Owner Type", sorted(data['owner'].unique()))

with col2:
    seller_type = st.selectbox("Seller Type", sorted(data['seller_type'].unique()))
    km_driven = st.number_input("KM Driven", min_value=0, value=10000, step=1000)
    car_age = st.number_input("Car Age (Years)", min_value=0, value=5)
    seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5)

col3, col4 = st.columns(2)
with col3:
    mileage = st.number_input("Mileage (km/l)", min_value=0.0, value=20.0, step=0.1)
    engine = st.number_input("Engine (cc)", min_value=0, value=1200)
with col4:
    max_power = st.number_input("Max Power (bhp)", min_value=0, value=80)

st.markdown("---")

# 4. Prediction Logic
if st.button("🔍 Predict Price", use_container_width=True, type="primary"):
    
    # ⚠️ CRITICAL FIX: The keys in this dictionary MUST exactly match the column 
    # names of the X_train data you used in your Jupyter Notebook.
    # Check your notebook and update the keys below if needed (especially 'mileage')!
    input_df = pd.DataFrame([{
        'name': name,
        'km_driven': km_driven,
        'fuel': fuel,
        'seller_type': seller_type,
        'transmission': transmission,
        'owner': owner,
        'mileage': mileage,  # <--- Double check if your notebook used 'mileage' or 'mileage(km/ltr/kg)'
        'engine': engine,
        'max_power': max_power,
        'seats': seats,
        'car_age': car_age
    }])

    try:
        prediction = model.predict(input_df)[0]
        st.success(f"### 💰 Estimated Selling Price: ₹{prediction:,.2f}")
    except Exception as e:
        st.error(f"️ Error: The model couldn't predict. This usually means the column names in the code don't match your training data. Details: {e}")
