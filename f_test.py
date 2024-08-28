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
#print(result)


from datetime import datetime

def format_date(date_str=None):
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format.
    
    If no date is provided, the current date is used.
    """
    if date_str is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    return date_obj.strftime("%d/%m/%Y")

# Example usage
 
print(format_date())              
