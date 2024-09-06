from flask import Flask, jsonify
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

app = Flask(__name__)

userID = 633258
apiKey = "71670dbab0aa7c87f4c3b8f4a29bce498e548a39"

zodiac_signs = [
    "aries", "taurus", "gemini", "cancer", 
    "leo", "virgo", "libra", "scorpio", 
    "sagittarius", "capricorn", "aquarius", "pisces"
]
timezone = 5.5

client = sdk.AstrologyAPIClient(userID, apiKey)

def get_zodiac_predictions():
    zodiac_cards = []

    messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable astrology assistant. Based on the user's prompt, provide predictions and call the relevant functions to generate these predictions."
        }
    ]

    for zodiacName in zodiac_signs:
        resource = f"sun_sign_prediction/daily/{zodiacName}"

        # Debug: Print the resource URL
        print(f"Requesting: {resource} for {zodiacName}")

        try:
            # Call the API for each zodiac sign
            dailyHoroResponse = client.dailyHoroCall(resource, zodiacName, timezone)

            if dailyHoroResponse.status_code == 200:
                # Parse the JSON data from the response
                dailyHoroData = dailyHoroResponse.json()
                prediction_date = dailyHoroData.get("prediction_date", "")
                if prediction_date:
                    formatted_date = datetime.strptime(prediction_date, "%m-%d-%Y").strftime("%d-%m-%Y")
                    dailyHoroData["prediction_date"] = formatted_date

                formatted_data = json.dumps(dailyHoroData, indent=4)

                # Prepare prompt for the LLM
                prompt = (
                    f"Based on the daily horoscope data for {zodiacName} on {formatted_date}, "
                    "provide insights and predictions using this date format {formatted_date}:\n\n"
                    "The following data is provided:\n\n"
                    f"{formatted_data}\n\n"
                    "Please summarize the data in a generalized manner, avoiding any astrology-specific terms. "
                    "The summary should be clear and concise, between 70 and 80 words. Focus on general advice and insights related to personal life, career, health, emotions, travel, and luck. Do not include any astrological terminology or specific references."
                )

                # Add user message for prompt
                messages.append({
                    "role": "user",
                    "content": prompt
                })

                # Generate prediction using OpenAI
                response = openai.chat.completions.create(
                    model=MODEL,
                    max_tokens=100,
                    temperature=0.7,
                    messages=messages
                )

                # Get the prediction from the response
                llm_predictions = response.choices[0].message.content

                # Append the zodiac sign card with fields reordered
                zodiac_cards.append({
                    "title": zodiacName.capitalize(),
                    "mediaType": "",  # Placeholder for media type
                    "mediaURL": "",  # Placeholder for media URL
                    "prediction": llm_predictions
                })

                # Remove user message to avoid overlapping in the next iteration
                messages.pop()

            else:
                zodiac_cards.append({
                    "title": zodiacName.capitalize(),
                    "mediaType": "",  # Placeholder for media type
                    "mediaURL": "",  # Placeholder for media URL
                    "prediction": f"Error: Received response with status code {dailyHoroResponse.status_code} for {zodiacName}. Response text: {dailyHoroResponse.text}"
                })
        except Exception as e:
            zodiac_cards.append({
                "title": zodiacName.capitalize(),
                "mediaType": "",  # Placeholder for media type
                "mediaURL": "",  # Placeholder for media URL
                "prediction": f"Exception occurred: {str(e)}"
            })

    return {
        "category": "zodiac",
        "categoryId": 1,
        "cards": zodiac_cards
    }

# Flask route to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({
        "data": [get_zodiac_predictions()]
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
