import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

# Load API key from .env file
load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

# Dataclass for current weather
@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

# Dataclass for daily weather forecast
@dataclass
class DailyWeather:
    day: str
    temperature: int
    main: str
    description: str
    icon: str

# Function to get latitude and longitude for a city
def get_lat_lon(city_name, country_code, API_key):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={API_key}'
    ).json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

# Function to get current weather data
def get_current_weather(lat, lon, API_key):
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    ).json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )
    return data

# Function to get weekly weather forecast
def get_weekly_forecast(lat, lon, API_key):
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_key}&units=metric'
    ).json()
    # # Debugging the API response
    # print(resp)  # Check the API response in your server console

    # if resp.get("cod") != 200:  # Check for API error
    #     print(f"API Error: {resp.get('message')}")
    #     return []  # Return empty list on error

    #check if daily key exists 
    if 'daily' not in resp:
        print("Error: 'daily' key not found in the response.")
        print(resp)
        return []
    
    daily_forecasts = []
    for day_data in resp['daily']:
        day = datetime.utcfromtimestamp(day_data['dt']).strftime('%A')
        day_weather = DailyWeather(
            day=day,
            temperature=int(day_data['temp']['day']),
            main=day_data['weather'][0]['main'],
            description=day_data['weather'][0]['description'],
            icon=day_data['weather'][0]['icon']
        )
        daily_forecasts.append(day_weather)
    return daily_forecasts


# Main function to get both current weather and weekly forecast
def main(city_name, country_code):
    lat, lon = get_lat_lon(city_name, country_code, api_key)
    current_weather = get_current_weather(lat, lon, api_key)
    weekly_forecast = get_weekly_forecast(lat, lon, api_key)
    return current_weather, weekly_forecast

if __name__ == '__main__':
    city_name = input("Enter the city name: ")
    country_code = input("Enter the country code (e.g., GB for Great Britain): ")
    current_weather, weekly_forecast = main(city_name, country_code)
    
    print(f"Current Weather in {city_name}, {country_code}:")
    print(f"{current_weather.main} - {current_weather.description}, {current_weather.temperature}°C")
    print("\n7-Day Forecast:")
    for day in weekly_forecast:
        print(f"{day.day}: {day.main} - {day.description}, {day.temperature}°C")