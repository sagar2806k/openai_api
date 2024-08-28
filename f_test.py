import json
import os
import requests

def check_matching_response(personId,partnerId,lang):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/matching/north-match"
    params = {
        "personId": personId,
        "partnerId": partnerId,
        "lang": lang
              }
    print("Here is the params:",params)
    response = requests.get(url, params=params)
    return {"personal_characteristics": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

result = check_matching_response(5,4,"en")
print(result)