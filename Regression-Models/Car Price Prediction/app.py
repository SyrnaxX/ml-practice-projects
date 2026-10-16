import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Car Price Predictor", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv("Cleaned car data.csv")

@st.cache_resource
def train_simple_model(df):
    # create simple numeric features + category -> mean-price encoding
    df = df.copy()
    y = df["selling_price"].astype(float)
    # numeric features
    num_cols = ["km_driven", "mileage(km/ltr/kg)", "engine", "max_power", "seats", "car_age"]
    X_num = df[num_cols].astype(float)
    # category mean-encoding
    cat_cols = ["name", "fuel", "transmission", "owner", "seller_type"]
    enc_maps = {c: df.groupby(c)["selling_price"].mean().to_dict() for c in cat_cols}
    # build encoded columns
    X_enc = pd.DataFrame({f"{c}_enc": df[c].map(enc_maps[c]) for c in cat_cols})
    X = pd.concat([X_num.reset_index(drop=True), X_enc.reset_index(drop=True)], axis=1)
    # fill any missing (just in case) with overall mean
    X = X.fillna(y.mean())
    model = LinearRegression()
    model.fit(X, y)
    return model, enc_maps, num_cols, [f"{c}_enc" for c in cat_cols]

df = load_data()
model, enc_maps, num_cols, enc_cols = train_simple_model(df)

st.title("Used Car Price Predictor (simple & fast)")

with st.form("input_form"):
    st.subheader("Car details")
    name = st.selectbox("Brand / Name", sorted(df["name"].unique()))
    fuel = st.selectbox("Fuel Type", sorted(df["fuel"].unique()))
    transmission = st.selectbox("Transmission", sorted(df["transmission"].unique()))
    owner = st.selectbox("Owner", sorted(df["owner"].unique()))
    seller_type = st.selectbox("Seller Type", sorted(df["seller_type"].unique()))

    st.subheader("Specs")
    km_driven = st.number_input("KM Driven", min_value=0, value=20000, step=1000)
    mileage = st.number_input("Mileage (km/l)", min_value=0.0, value=18.0, step=0.1)
    engine = st.number_input("Engine (cc)", min_value=0, value=1197)
    max_power = st.number_input("Max Power (bhp)", min_value=0.0, value=74.0, step=0.1)
    seats = st.number_input("Seats", min_value=2, max_value=10, value=5)
    car_age = st.number_input("Car Age (yrs)", min_value=0, max_value=30, value=5)

    submitted = st.form_submit_button("Predict")

if submitted:
    # build input row using same features used for training
    numeric = [km_driven, mileage, engine, max_power, seats, car_age]
    # map categories to mean price (fallback to overall mean)
    overall_mean = df["selling_price"].mean()
    cat_values = [
        enc_maps["name"].get(name, overall_mean),
        enc_maps["fuel"].get(fuel, overall_mean),
        enc_maps["transmission"].get(transmission, overall_mean),
        enc_maps["owner"].get(owner, overall_mean),
        enc_maps["seller_type"].get(seller_type, overall_mean),
    ]
    row = np.array(numeric + cat_values).reshape(1, -1)
    pred = model.predict(row)[0]
    st.success(f"Predicted selling price: ₹{pred:,.0f}")
    st.caption("This simple model is trained on the CSV at startup. For production, save a pipeline + model and load it instead.")
