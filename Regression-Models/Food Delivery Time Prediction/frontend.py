import streamlit as st
import requests
import json

# Page setup
st.set_page_config(page_title="Food Delivery Time Predictor", layout="wide")
st.title(" Food Delivery Time Prediction")
st.markdown("Enter order details to get estimated delivery time")

# Sidebar for inputs
with st.sidebar:
    st.header("Order Details")
    
    road_distance = st.number_input("Road Distance (km)", min_value=0.1, value=5.0, step=0.1)
    no_of_signals = st.number_input("Number of Signals", min_value=0, value=3, step=1)
    rider_rating = st.slider("Rider Rating", min_value=1.0, max_value=5.0, value=4.5, step=0.1)
    
    cuisine_type = st.selectbox("Cuisine Type", 
        ['Pizza', 'Desserts', 'Biryani', 'Burger', 'South Indian', 'Bakery', 'North Indian', 'Cafe', 'Chinese'])
    
    is_weekend = st.checkbox("Is Weekend?")
    is_festival = st.checkbox("Is Festival?")
    order_items = st.number_input("Number of Items", min_value=1, value=1, step=1)
    
    order_hour = st.text_input("Order Time(eg.2:45 PM)", value = "7:00 PM" )
    
    weather = st.selectbox("Weather", ['Clear', 'Rain', 'Cloudy', 'Storm', 'Fog'])
    pickup_zone = st.selectbox("Pickup Zone", ['CBD', 'Residential', 'Industrial', 'Commercial', 'Suburban'])
    dropoff_zone = st.selectbox("Dropoff Zone", ['Commercial', 'CBD', 'Residential', 'Industrial', 'Suburban'])
    vehicle_type = st.selectbox("Vehicle Type", ['Scooter', 'Bike', 'Electric Scooter', 'Bicycle'])
    traffic_level = st.selectbox("Traffic Level", ['Moderate', 'Low', 'High', 'Severe'])

# Main area
st.subheader("Prediction")

if st.button("🚀 Predict Delivery Time", type="primary"):
    # Prepare payload
    payload = {
        "Road_Distance_km": road_distance,
        "No_of_signals": no_of_signals,
        "Rider_Rating": rider_rating,
        "Cuisine_Type": cuisine_type,
        "Is_Weekend": is_weekend,
        "Is_Festival": is_festival,
        "Order_Items": order_items,
        "Order_Hour": order_hour,
        "Weather": weather,
        "Pickup_Zone": pickup_zone,
        "Dropoff_Zone": dropoff_zone,
        "Vehicle_Type": vehicle_type,
        "Traffic_Level": traffic_level
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"️ Predicted Delivery Time: {result} min")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to FastAPI server. Make sure it's running on port 8000!")

# Info section
with st.expander("ℹ️ About this Model"):
    st.write("""
    - *Model:* XGBoost Regressor
    - *R² Score:* 97.95%
    - *MAE:* ~3.97 minutes
    - *Features:* 14 
    """)