from flask import Flask, request, jsonify
import json
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MODEL = 'gpt-4o-mini'
api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"

app = Flask(__name__)


def personal_characteristics(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/personal-characteristics"
    params = {"personId": personId}
    print("Here is the personId:1",params)
    response = requests.get(url, params=params)
    return {"personal_characteristics": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

    

def ascendent_report(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/ascendant-report"
    params = {"personId": personId}
    print("Here is the personId:2",params)
    response = requests.get(url, params=params)
    return {"ascendent_report": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def mahadasha_predictions(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dashas/maha-dasha-predictions"
    params = {"personId": personId}
    print("Here is the personId:3",params)
    response = requests.get(url, params=params)
    return {"mahadasha_predictions": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def manglik_dosh(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/manglik-dosh"
    params = {"personId": personId}
    print("Here is the personId:4",params)
    response = requests.get(url, params=params)
    return {"manglik_dosh": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def kaalsarp_dosh(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/kaalsarp-dosh"
    params = {"personId": personId}
    print("Here is the personId:5",params)
    response = requests.get(url, params=params)
    return {"kaalsarp_dosh": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}


def run_conversation(user_prompt,person_Id):
    messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable astrology assistant. Based on the user's prompt, provide predictions and call the relevant functions to generate these predictions."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    tools = [
        {
    "type": "function",
    "function": {
        "name": "personal_characteristics",
        "description": "Based on the user's birth details, provide a personalized analysis of their personality traits, strengths, and weaknesses, also marriage details. Offer insights that can help them understand themselves better.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
},
       {
    "type": "function",
    "function": {
        "name": "ascendent_report",
        "description": "Generate a detailed report on the user's ascendant (rising sign), providing insights into their outward behavior, first impressions, and general demeanor.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "mahadasha_predictions",
        "description": "Provide predictions related to the Mahadasha period, offering insights into the significant life events and changes expected during this period based on Vedic astrology.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "manglik_dosh",
        "description": "Check for the presence of Manglik Dosh in the user's birth chart and provide relevant predictions regarding its effects on their life, particularly in marriage.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "kaalsarp_dosh",
        "description": "Analyze the user's birth chart to identify the presence of Kaalsarp Dosh and predict its impact on various aspects of their life, including challenges and remedies.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=MODEL,
        tools=tools,  
        tool_choice="required",
        max_tokens=4096,
    )

    response_message = response.choices[0].message

    tool_calls = getattr(response_message, 'tool_calls', None)
    print(f"{tool_calls}")

    print("Final response: ")

    if tool_calls:
        available_functions = {
            "personal_characteristics": personal_characteristics,
            "ascendent_report": ascendent_report,
            "mahadasha_predictions":mahadasha_predictions,
            "manglik_dosh":manglik_dosh,
            "kaalsarp_dosh":kaalsarp_dosh
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(personId=person_Id)
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                }
            )
            
            second_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content
    else:
        return response.choices[0].message.content
    

@app.route('/get-astrology-prediction', methods=['post'])
def get_astrology_prediction():
    data = request.get_json()

    person_id = data.get("person_id")
    user_details = data.get("user_details")
    user_prompt = data.get("user_prompt")

    full_prompt = f"""
  You are an astrology expert and will provide clear, positive, and easy-to-understand answers. Since the user might not be familiar with astrology, your responses should be simple, engaging, and maintain a positive tone.

  Tasks:
  Analyze the User's Question:

Determine the type of astrology prediction the user is asking for (e.g., daily sun, daily moon, weekly sun, weekly moon, yearly predictions, personal characteristics, or specific doshas like Manglik or Kaalsarp).
Identify and Call Relevant Functions:

Based on your analysis, call the appropriate function(s) using the user's birth details.
Ensure that all required parameters are included when calling these functions.
Handle Timeframes:

If the question specifies a time period (e.g., "this week," "next week," or a particular year), pass these as parameters when calling the functions.
Multiple Functions:

If the user's question covers multiple areas (e.g., a mix of personal characteristics and doshas), don't hesitate to call more than one function.
Instructions:
Respond Positively: Ensure that every response is optimistic and encouraging.
Simplify Astrology Concepts: Break down complex astrological terms and concepts into easy-to-understand language.
Maintain Clarity: Your responses should be straightforward and free of jargon.
Use these details to craft responses that are both insightful and accessible to the user.

    Here is the user's question: {user_prompt}.
    User's details: Date of birth: {user_details.get('dob')}, Time of birth: {user_details.get('tob')}, Latitude: {user_details.get('lat')}, Longitude: {user_details.get('lon')}, Time zone: {user_details.get('tz')}, Language: {user_details.get('lang')}
    If you cannot determine which function to call, always use the 'personal_characteristics' function.
    """

    prediction = run_conversation(full_prompt,person_id)

    response = {
        "person_id": person_id,
        "prediction": prediction,
        "error": None
    }

    return jsonify(response)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
     

