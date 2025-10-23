import requests
from config.settings import settings



class WeatherCollector:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = settings.weather_api_key

    def get_weather(self, city: str) -> dict:
        """Fetch current weather for a city"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Celsius
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout = 10
        )
        response.raise_for_status()
        return response.json()

    def parse_weather_data(self, raw_data: dict) -> dict:
        """Extract relevant fields from API response"""
        return {
            'city': raw_data['name'],
            'country': raw_data['sys']['country'],
            'temperature': raw_data['main']['temp'],
            'feels_like': raw_data['main']['feels_like'],
            'humidity': raw_data['main']['humidity'],
            'pressure': raw_data['main']['pressure'],
            'wind_speed': raw_data['wind']['speed'],
            'weather_main': raw_data['weather'][0]['main'],
            'weather_description': raw_data['weather'][0]['description']
        }