from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    country = Column(String)
    temperature = Column(Float)  # Celsius
    feels_like = Column(Float)
    humidity = Column(Integer)  # Percentage
    pressure = Column(Integer)  # hPa
    wind_speed = Column(Float)  # m/s
    weather_main = Column(String)  # e.g., "Clear", "Clouds"
    weather_description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<WeatherData(city={self.city}, temp={self.temperature}, time={self.timestamp})>"