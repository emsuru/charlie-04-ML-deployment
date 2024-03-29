# Description: This script  defines a basic FastAPI app with a root endpoint that returns "alive"
# and a /predict endpoint expecting property data and returning a real prediction (or mock prediction commented out)

# DISCLAIMER: IT's messy, I kept hitting errors especially on data encoding, will return to it to clean it up

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import os
from pydantic import BaseModel, Field
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)

# Import necessary functions from predict.py
from preprocessing.data_preprocessor import DataPreprocessor
from predict import load_preprocessor, load_model, clean_newdata, preprocess_newdata, predict as predict_function, save_predictions

app = FastAPI()

# Set port to the env variable PORT to make it easy to choose the port on the server
# If the Port env variable is not set, use port 8000
PORT = os.environ.get("PORT", 8000)
app = FastAPI(port=PORT)


# Defines a class named 'Property' which inherits from BaseModel (a class from the Pydantic library that provides data validation and parsing functionality)
# The class 'Property' has attributes that correspond to the expected input data for the model.
# Each attribute has a type annotation (e.g. int, str, float) and can have additional validation rules.

class Property(BaseModel):
    #Property model fields with default values
    id: Optional[int] = None
    price: Optional[int] = None
    # property_type: str = Field(None, pattern="^(HOUSE|APARTMENT)$")
    property_type: str = Field(pattern="^(HOUSE|APARTMENT)$", description="Type of the property: HOUSE or APARTMENT")
    subproperty_type: Optional[str] = None
    ## region: str = Field(None, pattern="^(Flanders|Wallonia|Brussels-Capital)$")
    region: str = Field(pattern="^(Flanders|Wallonia|Brussels-Capital)$", description="Region of the property: Flanders, Wallonia, or Brussels-Capital")
    province: Optional[str] = None
    locality: Optional[str] = None
    zip_code: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    construction_year: Optional[float] = None
    # total_area_sqm: float = Field(..., gt=0, lt=501)
    total_area_sqm: float = Field(..., gt=0, lt=501, description="Total area in square meters: must be greater than 0 and less than 501")
    surface_land_sqm: Optional[float] = None
    nbr_frontages: Optional[float] = None
    # nbr_bedrooms: int = Field(..., ge=1, le=7)
    nbr_bedrooms: int = Field(..., ge=1, le=7, description="Number of bedrooms: must be at least 1 and no more than 7")
    equipped_kitchen: Optional[str] = None
    fl_furnished: Optional[int] = None
    fl_open_fire: Optional[int] = None
    fl_terrace: Optional[int] = None
    terrace_sqm: Optional[float] = None
    fl_garden: Optional[int] = None
    garden_sqm: Optional[float] = None
    fl_swimming_pool: Optional[int] = None
    fl_floodzone: Optional[int] = None
    state_building: Optional[str] = None
    primary_energy_consumption_sqm: Optional[float] = None
    epc: Optional[str] = None
    heating_type: Optional[str] = None
    fl_double_glazing: Optional[int] = None
    cadastral_income: Optional[float] = None


@app.get("/")
async def root():
    """Route that return 'Alive!' if the server runs."""
    return {"Status": "Alive!"}

@app.get("/hello")
async def say_hello(user: str = "Anonymous"):
    """Route that will return 'hello {user}'."""
    return {"Message": f"Hello {user}!"}

@app.post("/predict")
def predict(property: Property):
    try:
        preprocessor_paths = {
            'onehotencoder': 'preprocessing/onehotencoder.pkl',
            'num_imputer': 'preprocessing/num_imputer.pkl',
            'columns_to_keep': 'preprocessing/columns_to_keep.pkl'
        }
        cleaned_data = clean_newdata(property.model_dump())
        preprocessed_data = preprocess_newdata(cleaned_data, preprocessor_paths)
        model = load_model('random_forest_model.pkl')  # Adjust path as necessary
        predictions = predict_function(model, preprocessed_data)
        logging.info(f"Predictions type: {type(predictions)}, value: {predictions}")
        # Extract the first element from the numpy array and convert it to a native Python type (float).
        prediction_value = float(predictions[0])
        # save_predictions(predictions, 'path/to/save/predictions')  # Optionally save predictions if needed
         # Now, safely pass this value to jsonable_encoder, though now it's not necessary, but for later if we need to return more than one value
        json_compatible_predictions = jsonable_encoder({"prediction": prediction_value})
        # json_compatible_predictions = jsonable_encoder({"prediction": predictions})
        logging.info(f"JSON-compatible Predictions: {json_compatible_predictions}")
        return json_compatible_predictions
        # logging.info(f"Predictions: {predictions}")
        # return {"prediction": predictions}
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    # return {"prediction": "Mock prediction: 200,000 EUR"} # mock return value to test out the API
