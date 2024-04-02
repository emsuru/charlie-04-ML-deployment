import streamlit as st
import requests

API_URL = "https://charlie-04-ml-deployment.onrender.com/predict"

st.title("Charlie ML - Price Predictor")

description = """
This app gives an estimated price for residential properties in Belgium.
The ML model behind it has been trained on a dataset of 70,000 real properties in Belgium.

The properties used for training were listed on the real estate website immoweb.be in February 2024.

Fill-in the form below to get a prediction.

"""
st.markdown(description)

# mandatory input fields as per the model 
property_type = st.selectbox("Property Type", ["HOUSE", "APARTMENT"])
st.caption("Select the type of property you're interested in.")
region = st.selectbox("Region", ["Flanders", "Wallonia", "Brussels-Capital"])
st.caption("Choose the region where the property is located.") 
total_area_sqm = st.slider("Surface (in m2)", min_value=0, max_value=500, step=1)
st.caption("Adjust the slider to the total area of the property in square meters.")
nbr_bedrooms = st.number_input("Bedrooms", min_value=0, max_value=7, step=1)
st.caption("Specify the number of bedrooms in the property, max 7.")

# Optional fields - set default values
default_values = {
  "id": 0,
  "price": 0,
  "subproperty_type": "string",
  "province": "string",
  "locality": "string",
  "zip_code": 0,
  "latitude": 0,
  "longitude": 0,
  "construction_year": 0,
  "surface_land_sqm": 0,
  "nbr_frontages": 0,
  "equipped_kitchen": "string",
  "fl_furnished": 0,
  "fl_open_fire": 0,
  "fl_terrace": 0,
  "terrace_sqm": 0,
  "fl_garden": 0,
  "garden_sqm": 0,
  "fl_swimming_pool": 0,
  "fl_floodzone": 0,
  "state_building": "string",
  "primary_energy_consumption_sqm": 0,
  "epc": "string",
  "heating_type": "string",
  "fl_double_glazing": 0,
  "cadastral_income": 0
}

if st.button("Predict Price"):
    # Construct the request payload
    payload = {
        "property_type": property_type,
        "region": region,
        "total_area_sqm": total_area_sqm,
        "nbr_bedrooms": nbr_bedrooms
    }
    # Update the payload with default values for optional fields
    payload.update(default_values)

    # Define the expected order of fields
    expected_order = [
        "id", "price", "property_type", "subproperty_type", "region", "province", "locality",
        "zip_code", "latitude", "longitude", "construction_year",
        "total_area_sqm", "surface_land_sqm", "nbr_frontages", "nbr_bedrooms",
        "equipped_kitchen",
        "fl_furnished", "fl_open_fire", "fl_terrace", "terrace_sqm",
        "fl_garden", "garden_sqm", "fl_swimming_pool", "fl_floodzone",
        "state_building", "primary_energy_consumption_sqm", "epc",
        "heating_type", "fl_double_glazing", "cadastral_income"
    ]

    # Reorder the payload according to the expected order
    ordered_payload = {key: payload.get(key) for key in expected_order}
    
    # Print the URL and payload for debugging
    print("Sending request to:", API_URL)
    print("Payload:", ordered_payload)

    # Make a POST request to the FastAPI service
    response = requests.post(API_URL, json=ordered_payload)

    # Print the status code and response for debugging
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    
    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"Predicted Price: {prediction} EUR")
    else:
        st.error("Error in prediction")


st.write("Made with ❤ by EmSuru.") 
st.write("To view the source code, visit the creator's [GitHub profile.](https://github.com/emsuru)")
