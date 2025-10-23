from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session
from typing import List
import requests

from app.database import engine, get_db, Base
from app.models import WeatherData
from app.schemas import WeatherDataResponse, WeatherDataCreate
from app.collector import WeatherCollector

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Analytics API")
collector = WeatherCollector()

@app.get("/")
def root():
    return {"message": "Weather Analytics API", "status": "running"}

@app.post("/collect/{city}", response_model=WeatherDataResponse)
def collect_weather(city: str, db: Session = Depends(get_db)):
    """Collect weather data for a specific city"""
    try:
        # Fetch from weather API
        raw_data = collector.get_weather(city)
        weather_data = collector.parse_weather_data(raw_data)

        # Save to database
        db_weather = WeatherData(**weather_data)
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)  # Get the ID and timestamp

        return db_weather


    except requests.exceptions.HTTPError as e:
        # API returned error status (404, 401, etc.)
        raise HTTPException(
            status_code=400,
            detail=f"Weather API error for city '{city}': {str(e)}"
        )

    except requests.exceptions.RequestException as e:
        # Network error, timeout, etc.
        raise HTTPException(
            status_code=503,
            detail=f"Failed to reach weather API: {str(e)}"
        )

    except Exception as e:
        # Database or other unexpected errors
        db.rollback()  # Undo any partial changes
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/weather/{city}", response_model=List[WeatherDataResponse], tags=["Query"])
def get_weather_history(
    city: str,
    limit: int = Query(default=10, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    weather_data = db.query(WeatherData) \
        .filter(WeatherData.city.ilike(f"%{city}%")) \
        .order_by(WeatherData.timestamp.desc()) \
        .limit(limit) \
        .all()

    if not weather_data:
        raise HTTPException(
            status_code=404,
            detail=f"No weather data found for city: {city}"
        )

    return weather_data

@app.get("/weather/", response_model=List[WeatherDataResponse], tags=["Query"])
def get_all_weather(
    limit: int = Query(default=20, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    weather_data = db.query(WeatherData) \
        .order_by(WeatherData.timestamp.desc()) \
        .limit(limit) \
        .all()

    return weather_data