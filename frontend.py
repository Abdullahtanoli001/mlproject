import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("House Price Predictor")
st.markdown("Enter your details below")

bedrooms= st.number_input("Bedrooms")
bathrooms= st.number_input("Bathrooms")
sqft_living= st.number_input("sqft_living")
sqft_lot= st.number_input("sqft_lot")
floors= st.number_input("floors")
condition= st.number_input("condition")
city = st.selectbox("City", ["Seattle", "Redmond", "Bellevue", "Kirkland"])

if st.button("Predict Price"):
    input_data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "condition": condition,
        "city": city
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200:
            st.success(f"Predicted Price: **{result['predicted_price']}**")
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server.")
