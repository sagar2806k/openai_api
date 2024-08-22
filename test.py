from flask import Flask, request, jsonify
import json
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime


load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MODEL = 'gpt-4o-mini'

app = Flask(__name__)

def astrology_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        data = response.json()
        #print("jason data==========",data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        print("Response Content:", response.content)
        raise Exception(f"Failed to fetch data from API: {e}")

def format_date(date_str):
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")

    
def multiple_api_callings(user_prompt,personId,lang):
    api_urls = {
        "personal_characteristics": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/personal-characteristics?personId={personId}&lang={lang}",
        "ascendent_report": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/ascendant-report?personId={personId}&lang={lang}",
        "mahadasha_predictions":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dashas/maha-dasha-predictions?personId={personId}&lang={lang}",
        "manglik_dosh":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/manglik-dosh?personId={personId}&lang={lang}",
        "kaalsarp_dosh":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/kaalsarp-dosh?personId={personId}&lang={lang}"
    }

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
        "description": "Based on the user's birth details, provide a personalized analysis of their personality traits, strengths, and weaknesses, and marriage details. Offer insights that can help them understand themselves better.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the user's birth details."
                }
            },
            "required": ["api_url"]
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
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the user's birth details and ascendant information."
                }
            },
            "required": ["api_url"]
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
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the user's birth details and Mahadasha information."
                }
            },
            "required": ["api_url"]
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
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the user's birth details and Manglik Dosh information."
                }
            },
            "required": ["api_url"]
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
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the user's birth details and Kaalsarp Dosh information."
                }
            },
            "required": ["api_url"]
        }
    }
},
{
            "type": "function",
            "function": {
                "name": "weekly_sun",
                "description": "Provide weekly sun predictions based on the specified week.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "api_url": {
                            "type": "string",
                            "description": "URL or unique identifier for accessing the weekly sun predictions."
                        },
                        "week": {
                            "type": "string",
                            "enum": ["thisweek", "nextweek"],
                            "description": "Specify the week for which predictions are needed."
                        },
                        "split": {
                            "type": "boolean",
                            "description": "Specify whether the prediction should be split into sections or not.",
                            "default": True
                        }
                    },
                    "required": ["api_url", "week"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "weekly_moon",
                "description": "Provide weekly sun predictions based on the specified week.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "api_url": {
                            "type": "string",
                            "description": "URL or unique identifier for accessing the weekly sun predictions."
                        },
                        "week": {
                            "type": "string",
                            "enum": ["thisweek", "nextweek"],
                            "description": "Specify the week for which predictions are needed."
                        },
                        "split": {
                            "type": "boolean",
                            "description": "Specify whether the prediction should be split into sections or not.",
                            "default": True
                        }
                    },
                    "required": ["api_url", "week"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "daily_sun",
                "description": "Provide daily sun predictions based on the specified date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "api_url": {
                            "type": "string",
                            "description": "URL or unique identifier for accessing the daily sun predictions."
                        },
                        "date": {
                            "type": "string",
                            "description": "Specify the date for which predictions are needed."
                        },
                        "split": {
                            "type": "boolean",
                            "description": "Specify whether the prediction should be split into sections or not.",
                            "default": True
                        }
                    },
                    "required": ["api_url", "date"]
                }
            }
        },
         {
            "type": "function",
            "function": {
                "name": "daily_moon",
                "description": "Provide daily moon predictions based on the specified date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "api_url": {
                            "type": "string",
                            "description": "URL or unique identifier for accessing the daily moon predictions."
                        },
                        "date": {
                            "type": "string",
                            "description": "Specify the date for which predictions are needed."
                        },
                        "split": {
                            "type": "boolean",
                            "description": "Specify whether the prediction should be split into sections or not.",
                            "default": True
                        }
                    },
                    "required": ["api_url", "date"]
                }
            }
        },
        {
    "type": "function",
    "function": {
        "name": "yearly_predictions",
        "description": "Provide yearly predictions based on the specified year.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {
                    "type": "string",
                    "description": "URL or unique identifier for accessing the yearly predictions."
                },
                "year": {
                    "type": "string",
                    "description": "Specify the year for which predictions are needed."
                }
            },
            "required": ["api_url", "year"]
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

    print("LLM Initial Response:", response)
    print("===========================================================")

    response_message = response.choices[0].message
    print(f"{response_message}")

    print("===========================================================")

    tool_calls = getattr(response_message, 'tool_calls', [])
    print(f"{tool_calls}")

    print("===========================================================")

    if tool_calls:
        available_functions = {
            "personal_characteristics": astrology_data,
            "ascendent_report": astrology_data,
            "mahadasha_predictions":astrology_data,
            "manglik_dosh":astrology_data,
            "kaalsarp_dosh":astrology_data,
            "weekly_sun" :astrology_data,
            "weekly_moon":astrology_data,
            "daily_sun": astrology_data,
            "daily_moon": astrology_data,
            "yearly_predictions":astrology_data

        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            date = function_args.get("date")
            split = function_args.get("split", True)
            formatted_date = format_date(date) if date else date
            year = function_args.get("year")

            print("================ Arguments",function_args)

            if function_name == "weekly_sun":
                api_url = f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/weekly-sun?personId={personId}&week={function_args['week']}&split={str(split).lower()}&lang={lang}"
            elif function_name == "weekly_moon":
                api_url = f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/weekly-moon?personId={personId}&week={function_args['week']}&split={str(split).lower()}&lang={lang}"
            elif function_name == "daily_sun":
                api_url = f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/daily-sun?personId={personId}&date={formatted_date}&split={str(split).lower()}&lang={lang}"
            elif function_name == "daily_moon":
                api_url = f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/daily-moon?personId={personId}&date={formatted_date}&split={str(split).lower()}&lang={lang}"
            elif function_name == "yearly_predictions":
                api_url =f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/prediction/yearly?personId={personId}&year={year}&lang={lang}"
            else:
                api_url = api_urls.get(function_name)
                
            function_response = function_to_call(api_url)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="none"
        )
        return second_response.choices[0].message.content

@app.route('/get-astrology-prediction', methods=['post'])
def get_astrology_prediction():
    data = request.get_json()

    personId = data.get("personId")
    user_details = data.get("user_details")
    lang= data.get("lang")
    user_prompt = data.get("user_prompt")

    full_prompt = f"""
  You are an astrology expert tasked with providing clear, concise, and positive predictions. Your responses should be short (100-250 words), easy to understand, and focused on actionable insights and recommendations for the user.

Tasks:
1. **Analyze the User's Question:**
   - Determine the type of astrology prediction needed (e.g., daily, weekly, yearly predictions, personal characteristics, or specific doshas like Manglik or Kaalsarp).
   - Call the appropriate function(s) using the user's birth details. Ensure all necessary parameters are included.

2. **Avoid Complex Astrology Terms:**
   - Do not use technical terms lik ries,' '12th house,' '7th lord,' or similar. Focus on simple language.

3. **Provide Practical Insights:**
   - Offer predictions that include recommendations, conclusions, and actionable points.
   - Encourage the user to ask more questions based on your output.

Instructions:
- **Positive Tone:** Ensure every response is optimistic and encouraging.
- **Clarity:** Break down astrology concepts into simple, understandable terms.
- **Action-Oriented:** Provide predictions in a point-wise format that guides the user on what steps to take next.
- **Do not give long long response make sure the response is based on only user question(prompt).
- **Based on user question if you need to call 2 or 3 function then call it. 
    In short if "necessary" to call multiple function then do not hesitate.
- ** If question is out of all of these 10 function then do not give wrong answer.
-** Whenever user ask for zodiac sign or rashi you need to consider user_details.get("kundali)
- **Handle Incorrect Questions:** If the question is outside the scope of the available functions, provide a response indicating that the question cannot be addressed with the available functions without giving additional incorrect information.

Here is the user's question: {user_prompt}.
User's details: Date of birth: {user_details.get('dob')}, Time of birth: {user_details.get('tob')}, Latitude: {user_details.get('lat')}, Longitude: {user_details.get('lon')}, Time zone: {user_details.get('tz')}, 
lang: {lang}.

If you are uncertain about which function to call, use the 'personal_characteristics' function by default.
    """

    prediction = multiple_api_callings(full_prompt,personId,lang)

    response = {
        "personId": personId,
        "prediction": prediction
    }

    return jsonify(response)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
     
