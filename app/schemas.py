from pydantic import BaseModel
from datetime import datetime

class WeatherDataCreate(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    weather_main: str
    weather_description: str


class WeatherDataResponse(WeatherDataCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True