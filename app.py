#This code defines a basic FastAPI app with a root endpoint that returns "alive" 
# and a /predict endpoint expecting property data and returning a mock prediction.

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
     
app = FastAPI()

class Property(BaseModel):
    LivingArea: int
    TypeOfProperty: str
    Bedrooms: int
    PostalCode: int
    SurfaceOfGood: Optional[int] = None
    # Add other fields as necessary

@app.get("/")
def read_root():
    return {"message": "alive"}

@app.post("/predict")
def predict(property: Property):
    # Here you would load your model and make a prediction
    # For now, let's just return a mock prediction
    return {"prediction": 123456.78}