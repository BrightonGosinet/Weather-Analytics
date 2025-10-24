"""
Data collection script for weather analytics.
Run this periodically to build up weather history.
"""

from app.collector import WeatherCollector
from app.database import SessionLocal
from app.models import WeatherData
import time

def collect_cities():
    """Collect weather data for multiple cities."""

    cities = [
        'Edmonton',
        'Calgary',
        'Vancouver',
        'Toronto',
        'Montreal',
        'New York',
        'London',
        'Tokyo',
        'Paris',
        'Sydney'
    ]

    collector = WeatherCollector()
    db = SessionLocal()

    success_count = 0

    try:
        for city in cities:
            try:
                # Fetch weather data
                raw_data = collector.get_weather(city)
                weather_data = collector.parse_weather_data(raw_data)

                # Save to database
                db_weather = WeatherData(**weather_data)
                db.add(db_weather)

                print(f"{city:15s} - {weather_data['temperature']}°C - {weather_data['weather_description']}")
                success_count += 1

                # Delay to avoid rate limiting
                time.sleep(1)

            except Exception as e:
                print(f"{city:15s} - Error: {str(e)}")

        db.commit()
        print(f"\nCollection complete! {success_count}/{len(cities)} cities saved successfully.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    collect_cities()
