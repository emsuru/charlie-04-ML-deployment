#This code defines a basic FastAPI app with a root endpoint that returns "alive"
# and a /predict endpoint expecting property data and returning a mock prediction.

from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel, Field
from typing import Optional

# Import necessary functions from predict.py
from predict import load_preprocessor, load_model, clean_newdata, preprocess_newdata, predict as predict_function, save_predictions

app = FastAPI()

# This line defines a class named 'Property' which inherits from BaseModel.
# BaseModel is a class provided by Pydantic, used here to define data models where the types of the attributes are validated.
# In this context, it allows us to create a data model for 'Property' with type annotations, ensuring that instances of Property have attributes of correct types.
# An object instance of this class when instantiated would look like Property(id=123, price=250000, property_type="House", subproperty_type="Villa", region="West", province="Province A", locality="Locality X", zip_code=12345, latitude=50.1234, longitude=4.5678, construction_year=1990, total_area_sqm=120.5, surface_land_sqm=200.0, nbr_frontages=2.0, nbr_bedrooms=3, equipped_kitchen="Installed", fl_furnished=0, fl_open_fire=1, fl_terrace=1, terrace_sqm=15.0, fl_garden=1, garden_sqm=100.0, fl_swimming_pool=0, fl_floodzone=0, state_building="Good", primary_energy_consumption_sqm=250.0, epc="B", heating_type="Gas", fl_double_glazing=1, cadastral_income=1500.0)
class Property(BaseModel):
    #Property model fields with default values
    id: Optional[int] = None
    price: Optional[int] = None
    property_type: str = Field(None, regex="^(HOUSE|APARTMENT)$")
    subproperty_type: Optional[str] = None
    region: Optional[str] = None
    province: Optional[str] = None
    locality: Optional[str] = None
    zip_code: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    construction_year: Optional[float] = None
    total_area_sqm: Optional[float] = None
    surface_land_sqm: Optional[float] = None
    nbr_frontages: Optional[float] = None
    nbr_bedrooms: Optional[int] = None
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
