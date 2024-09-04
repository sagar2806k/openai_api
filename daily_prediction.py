import requests
import openai
import os
from dotenv import load_dotenv
import sdk
import json
from datetime import datetime


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
MODEL = 'gpt-4o-mini'

messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable astrology assistant. Based on the user's prompt, provide predictions and call the relevant functions to generate these predictions."
        }
]
userID = 632493
apiKey = "05ab3143c0b2f253b2192d2f20f5ac9bc383d664"

zodiacName = "taurus"
timezone = 5.5

resource = "sun_sign_prediction/daily/" + zodiacName

client = sdk.AstrologyAPIClient(userID, apiKey)

# Call the API and get the response object
dailyHoroResponse = client.dailyHoroCall(resource, zodiacName, timezone)

# Check if the response is successful
if dailyHoroResponse.status_code == 200:
    try:
        # Parse the JSON data from the response
        dailyHoroData = dailyHoroResponse.json()
        prediction_date = dailyHoroData.get("prediction_date", "")
        if prediction_date:
            # Convert the date from m-d-yyyy to datetime object and then to dd-mm-yyyy
            formatted_date = datetime.strptime(prediction_date, "%m-%d-%Y").strftime("%d-%m-%Y")
            dailyHoroData["prediction_date"] = formatted_date

        formatted_data = json.dumps(dailyHoroData, indent=4)
        print("Formatted Data to Send to LLM:")
        print(formatted_data)

        prompt = (
    f"Based on the daily horoscope data for {zodiacName} on {formatted_date}, "
    "provide insights and predictions using this date format {formatted_date}:\n\n"
    "The following data is provided:\n\n"
    f"{formatted_data}\n\n"
    "Please summarize the data in a generalized manner, avoiding any astrology-specific terms. "
    "The summary should be clear and concise, between 70 and 80 words. Focus on general advice and insights related to personal life, career, health, emotions, travel, and luck. Do not include any astrological terminology or specific references."
)

        messages.append({
            "role": "user",
            "content": prompt
        })


        response = openai.chat.completions.create(
            model = MODEL,
            max_tokens = 100,
            temperature = 0.7,
            messages = messages
        )

        llm_predictions = response.choices[0].message.content
        print("Generated Prediction:")
        print(llm_predictions)

    except json.JSONDecodeError:
        print("Failed to parse the response JSON.")
else:
     print(f"Error: Received response with status code {dailyHoroResponse.status_code}")
