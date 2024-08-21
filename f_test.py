import json
import os
import requests

def daily_sun(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/daily-sun"
    params = {"personId": personId,"date": "date","split":True}
    response = requests.get(url, params=params)
    return {"daily_sun": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

response1 = daily_sun(1)
print(response1)
