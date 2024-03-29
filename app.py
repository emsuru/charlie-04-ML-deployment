#This code defines a basic FastAPI app with a root endpoint that returns "alive"
# and a /predict endpoint expecting property data and returning a mock prediction.

from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
from typing import Optional

# Import necessary functions from predict.py
from predict import load_preprocessor, load_model, clean_newdata, preprocess_newdata, predict as predict_function, save_predictions

app = FastAPI()

class Property(BaseModel):
    #Property model fields
    id: int
    price: int
    property_type: str
    subproperty_type: str
    region: str
    province: str
    locality: str
    zip_code: int
    latitude: float
    longitude: float
    construction_year: float
    total_area_sqm: float
    surface_land_sqm: float
    nbr_frontages: float
    nbr_bedrooms: int
    equipped_kitchen: str
    fl_furnished: int
    fl_open_fire: int
    fl_terrace: int
    terrace_sqm: float
    fl_garden: int
    garden_sqm: float
    fl_swimming_pool: int
    fl_floodzone: int
    state_building: str
    primary_energy_consumption_sqm: float
    epc: str
    heating_type: str
    fl_double_glazing: int
    cadastral_income: float

   # this is how I should define all fields, providing a default value if needed:
    #SurfaceOfGood: Optional[int] = None  # Defines an optional integer field for SurfaceOfGood, defaulting to None if not provided

# Set port to the env variable PORT to make it easy to choose the port on the server
# If the Port env variable is not set, use port 8000
PORT = os.environ.get("PORT", 8000)
app = FastAPI(port=PORT)


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
    # try:
    #     # Assuming property is a dictionary that matches the expected input format
    #     # You might need to adjust this part based on how your prediction logic expects inputs
    #     cleaned_data = clean_newdata(property.dict())
    #     preprocessed_data = preprocess_newdata(cleaned_data, preprocessor_paths)
    #     model = load_model('path/to/your/model.pkl')  # Adjust path as necessary
    #     predictions = predict_function(model, preprocessed_data)
    #     # Optionally save predictions if needed
    #     # save_predictions(predictions, 'path/to/save/predictions')
    #     return {"prediction": predictions}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    return {"prediction": "Mock prediction: 200,000 EUR"}
