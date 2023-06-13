import requests
from configparser import ConfigParser
import json

config = ConfigParser()
config.read('./secrets.cfg')

x_app_id = config['nutritionix']['API_ID']
x_app_key = config['nutritionix']['API_KEY']

headers = {
    'Accept':'application/json',
    'Content-Type': 'application/json',
    "x-app-id": str(x_app_id),
    "x-app-key": str(x_app_key),
}


url = 'https://trackapi.nutritionix.com/v2/natural/nutrients/'

def get_calories(prompt: str):
    req = requests.post(url, headers=headers, json={"query": prompt})
    food_details = req.json()
    calories = food_details['foods'][0]['nf_calories']
    return calories