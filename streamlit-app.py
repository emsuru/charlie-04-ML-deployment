import streamlit as st
import requests

API_URL = "https://charlie-04-ml-deployment.onrender.com/predict"

st.title("Sale Price Predictor")

# mandatory input fields as per the model 
property_type = st.selectbox("Property Type", ["HOUSE", "APARTMENT"])
region = st.selectbox("Region", ["Flanders", "Wallonia", "Brussels-Capital"])
total_area_sqm = st.number_input("Surface (in m2)", min_value=0, max_value=500, step=1)
nbr_bedrooms = st.number_input("Bedrooms", min_value=0, max_value=7, step=1)

# Optional fields - set default values
default_values = {
    "id": None,
    "price": None,
    "subproperty_type": None,
    "province": None,
    "locality": None,
    "zip_code": None,
    "latitude": None,
    "longitude": None,
    "construction_year": None,
    "surface_land_sqm": None,
    "nbr_frontages": None,
    "equipped_kitchen": None,
    "fl_furnished": None,
    "fl_open_fire": None,
    "fl_terrace": None,
    "terrace_sqm": None,
    "fl_garden": None,
    "garden_sqm": None,
    "fl_swimming_pool": None,
    "fl_floodzone": None,
    "state_building": None,
    "primary_energy_consumption_sqm": None,
    "epc": None,
    "heating_type": None,
    "fl_double_glazing": None,
    "cadastral_income": None
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

st.write("Made with ❤ by EmSuru")
