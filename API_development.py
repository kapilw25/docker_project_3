# Implement the /collect endpoint to accept and store data.
# Implement the /analyze endpoint to query the database and return basic statistics.
# Implement the /predict endpoint to make predictions using the machine learning model.

# the /collect endpoint needs to accept data relevant to the retail dataset. 
# The /analyze endpoint could provide insights such as total sales, most popular products, or customer activity.

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import joblib
from database_setup import get_db, RetailData # ensure that the database_setup.py file is in the same directory as this file.
from sqlalchemy import func
import toml

app = FastAPI()

# Load the configuration from secrets.toml
config = toml.load('secrets.toml')
api_secret_key = config["api"]["secret_key"]
# Load the model.
model = joblib.load('model.joblib')

# API Key Authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# Define Pydantic models for data validation.
class RetailDataModel(BaseModel):
    invoice: str
    stock_code: str
    description: str
    quantity: int
    invoice_date: datetime
    price: float
    customer_id: float
    country: str
    
    class Config:
        from_attribute = True
        

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != api_secret_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header
        
@app.post("/collect/", dependencies=[Depends(get_api_key)])
def collect_retail_data(item: RetailDataModel, db: Session = Depends(get_db)):
    # Create a new retail data record.
    db_item = RetailData(**item.dict())
    db.add(db_item)
    db.commit()
    return {"message": "Retail Data collected successfully."}

@app.get("/analyze/")
def analyze_data(db: Session = Depends(get_db)):
    # Example analysis: total sales.
    total_sales = db.query(func.sum(RetailData.price * RetailData.quantity)).scalar()
    return {"total_sales": total_sales}

class PredictionRequest(BaseModel):
    price: float
    day_of_week: int
    month: int
    
@app.post("/predict/")
def predict_engagement(request: PredictionRequest):
    # Use the model to make a prediction.
    features = [[request.price, request.day_of_week, request.month]]
    prediction = model.predict(features)
    return {"prediction_quantity": prediction[0]}
        

