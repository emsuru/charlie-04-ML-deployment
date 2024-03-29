#This code defines a basic FastAPI app with a root endpoint that returns "alive"
# and a /predict endpoint expecting property data and returning a mock prediction.

from fastapi import FastAPI
import os
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
    # Here you would load your model and make a prediction
    # For now, let's just return a mock prediction
    return {"prediction": 123456.78}
