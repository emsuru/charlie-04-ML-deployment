# Immo Charlie Phase 04: Deployment

![docker](https://img.shields.io/badge/Docker-3.3.0-blue)
![fastapi](https://img.shields.io/badge/FastAPI-0.68.0-green)
![render](https://img.shields.io/badge/Render-0.1.0-orange)

This app deploys the Price Prediction ML model built [here](https://github.com/emsuru/charlie-03-ML-training).

The model is containerized with Docker and offered to:
- **developers** via a RESTful API with FastAPI and hosted on Render here: https://charlie-04-ml-deployment.onrender.com/docs
- **non-technical users** via a simple web app here: https://charlie-ml.streamlit.app/

## Developer API 

- **API endpoint**: https://charlie-04-ml-deployment.onrender.com/docs  Please note that I'm using the free hosting service from Render, which means it may take up to 1 minute or more for the page to load if it hasn't been called in a while. 

- **Method**: POST

- **Endpoint**: `/predict`

- **Request Body**: JSON format containing property details

- **Response**: JSON format with the predicted price

Scroll down to the bottom of the /docs page to find the API schema for `/property`, with indication of optional/mandatory parameters and the required value types to be used.

## Example Request:

```

{
  "id": 0,
  "price": 0,
  "property_type": "HOUSE",
  "subproperty_type": "string",
  "region": "Flanders",
  "province": "string",
  "locality": "string",
  "zip_code": 0,
  "latitude": 0,
  "longitude": 0,
  "construction_year": 0,
  "total_area_sqm": 120,
  "surface_land_sqm": 0,
  "nbr_frontages": 0,
  "nbr_bedrooms": 3,
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

```

## Example Response:

```

{
  "prediction": 345708.14
}

```

---

## Web application

For a non-technical user persona I have set up a small web app using Streamlit that is live here: 

https://charlie-ml.streamlit.app/

Please note that it may take a while to load. 
