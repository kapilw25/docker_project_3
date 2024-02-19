import streamlit as st
import requests
import datetime
import toml

# Load the configuration from secrets.toml
config = toml.load('secrets.toml')
api_secret_key = config["api"]["secret_key"]

st.title("Retail Data Collection and Analysis")

# input form for the user to input retail data
with st.form(key='predict_form'):
    st.header('Enter the details for prediction:')
    price = st.number_input('Price', min_value=0.0, format='%f')
    day_of_week = st.selectbox('Day of the week', (0, 1, 2, 3, 4, 5, 6))
    month = st.selectbox('Month', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    submit_button = st.form_submit_button(label='Predict')
    
# if the user clicks the predict button, make a POST request to the API
if submit_button:
    # api_endpoint = "http://127.0.0.1:8000/predict/"
    api_endpoint = "http://api:8000/predict/"
    data = {
        "price": price,
        "day_of_week": day_of_week,
        "month": month
    }
    
    headers = {
        "X-API-Key": api_secret_key,
        'Content-Type': 'application/json'
    }
    
    # make the POST request to the API
    response = requests.post(api_endpoint, json=data, headers=headers)
    
    # if the request is successful, display the prediction
    if response.status_code == 200:
        prediction = response.json()['prediction_quantity']
        st.success(f"The predicted quantity of products sold is {prediction}.")
    else:
        st.error("An error occurred while making the prediction.")