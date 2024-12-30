import streamlit as st
import numpy as np
from joblib import load

# Load the model
regressor = load('model.pkl')

def show_predict_page():
    st.title('Car Resale Value Prediction')

    st.write("""### Please fill in the required information: """)

    # Sample dropdowns and inputs
    selected_brand = st.selectbox("Brand", ["BrandA", "BrandB", "BrandC"])
    selected_year = st.selectbox("Year", [2010, 2011, 2012, 2013, 2014, 2015])
    selected_mileage = st.slider("Mileage", 10000, 300000, 50000)
    selected_transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

    # Map inputs to numeric values
    brand_mapping = {"BrandA": 0, "BrandB": 1, "BrandC": 2}
    transmission_mapping = {"Manual": 0, "Automatic": 1}

    encoded_brand = brand_mapping[selected_brand]
    encoded_transmission = transmission_mapping[selected_transmission]

    # Prepare input for the model
    input_data = np.array([[encoded_brand, selected_year, selected_mileage, encoded_transmission]])

    if st.button("Predict Resale Value"):
        try:
            # Make a prediction
            predicted_price = regressor.predict(input_data)
            st.subheader(f'The estimated resale value is RM{predicted_price[0]:.2f}')
        except Exception as e:
            st.error(f"An error occurred: {e}")

show_predict_page()
