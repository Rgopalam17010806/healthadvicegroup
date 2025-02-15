import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
import requests

from website.views import airquality

#create a blueprint for the air quality endoint
airquality = Blueprint('air_quality', __name__)

# Load the environment variable
load_dotenv()
api_key = os.getenv('AIR_QUALITY_API_KEY')

# Get data
@airquality.route('api/data', methods=['GET'])
def get_data():
    location = request.args.get('location') #get the location 
    api_key = os.getenv('AIR_QUALITY_API_KEY') #Load the API key

    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={api_key}'
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json() #parse the rsponse to JSON data 

    if not geo_data or len(geo_data) == 0:
        return jsonify({"error": "Location not found"}), 404

    lat = geo_data[0]['lat'] #extract the latitude and longitude from the response dara
    lon = geo_data[0]['lon']

    aqi_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    aqi_response = requests.get(aqi_url)
    aqi_data = aqi_response.json()

    return jsonify(aqi_data) #returns the AQI Data as a JSON Response