from flask import Flask, request,jsonify,Response
import json
import os
import requests
from dotenv import load_dotenv
import openai
from datetime import datetime,timedelta

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



MODEL = 'gpt-4o'

app = Flask(__name__)

def astrology_data(api_url):
    try:
        print("===========================================================")
        print(f"Calling astrology_data with URL: {api_url}")
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
    print(f"Formatting date: {date_str}")
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")


def get_current_and_next_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    next_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Current date: {current_date}, Next date: {next_date}")
    return current_date, next_date

current_date, next_date = get_current_and_next_date()


def multiple_api_callings(user_prompt,personId,lang,partnerId):

    api_urls = {
        "personal_characteristics": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/personal-characteristics?personId={personId}&lang={lang}",
        "ascendent_report": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/ascendant-report?personId={personId}&lang={lang}",
        "mahadasha_predictions":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dashas/maha-dasha-predictions?personId={personId}&lang={lang}",
        "manglik_dosh":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/manglik-dosh?personId={personId}&lang={lang}",
        "kaalsarp_dosh":f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/kaalsarp-dosh?personId={personId}&lang={lang}",
        "north_match": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/matching/north-match?personId={personId}&partnerId={partnerId}&lang={lang}",
        "dashakoot" : f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/matching/dashakoot?personId={personId}&partnerId={partnerId}&lang={lang}",
        "aggregate_match": f"https://astrology-backend-ddcz.onrender.com/api/v1/api-function/matching/aggregate-match?personId={personId}&partnerId={partnerId}&lang={lang}"
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
},
{
    "type": "function",
    "function": {
        "name": "north_match",
        "description": "Provide compatibility analysis between two individuals based on their astrological charts using the Indian astrology system.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {
                    "type": "string",
                    "description": "URL for accessing the compatibility report between two individuals."
                }
            },
            "required": ["api_url"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "dashakoot",
        "description": "Provide compatibility analysis between two individuals based on their Dashakoot compatibility score using the Indian astrology system.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {
                    "type": "string",
                    "description": "URL for accessing the Dashakoot compatibility report between two individuals."
                }
            },
            "required": ["api_url"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "aggregate_match",
        "description": "Provide a comprehensive compatibility analysis between two individuals by aggregating various astrological factors.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {
                    "type": "string",
                    "description": "URL for accessing the aggregate compatibility report between two individuals."
                }
            },
            "required": ["api_url"]
        }
    }
}

    ]

    response = openai.chat.completions.create(
        messages=messages,
        model=MODEL,
        tools=tools,  
        tool_choice="required",
        max_tokens=4096,
        temperature=0.5
    )

    print("LLM Initial Response:", response)
    print("============================================================")

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
            "yearly_predictions":astrology_data,
            "north_match": astrology_data,
            "dashakoot": astrology_data,
            "aggregate_match": astrology_data

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

            

        second_response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="none",
            temperature=0.5
        )
        return second_response.choices[0].message.content

@app.route('/get-astrology-prediction', methods=['post'])
def get_astrology_prediction():
    data = request.get_json()

    personId = data.get("personId")
    partnerId = data.get("partnerId")
    user_details = data.get("user_details")
    partner_details = data.get("partner_details")
    lang= data.get("lang")
    user_prompt = data.get("user_prompt")

    full_prompt = f"""
  You are an astrology expert tasked with providing clear, concise, and positive predictions. 
  Your responses should be short, easy to understand, and focused on actionable insights and recommendations for the user.

Tasks:
Analyze the User's Question:

Determine the type of astrology prediction needed (e.g., daily, weekly, yearly predictions, personal characteristics, or specific doshas like Manglik or Kaalsarp).
Identify the user's needs based on their question and use the appropriate function(s) with the necessary birth details.
Avoid Complex Astrology Terms:

Avoid using technical astrology jargon. Explain concepts in simple, everyday language that anyone can understand.
Provide Practical Insights:

Offer predictions that include recommendations, conclusions, and actionable points.
Frame every response with positivity and encouragement, focusing on actionable advice that helps the user take practical steps in their life.
Encourage the user to ask more questions based on your output.
Partner-Related Questions:

For questions related to a partner, spouse, or significant other, use both the user's and partner's details.
If partner details are missing or incomplete, politely ask the user to provide them (e.g., "Could you please share your partner's details?" or "Select your partner's profile").
Use functions like north_match, aggregate_match, and dashakoot as needed based on the question. It is not necessary to call all three functions every time; instead, choose the relevant functions based on the user's query.
Respond in Selected Language:

Always respond in the language chosen by the user, even if the question is asked in a different language. Prioritize the selected language for clarity and consistency.

******Instructions******

Respond to Greetings:
Reply to greetings with a friendly and time-appropriate message, such as "Good morning! How can I assist you today?" without invoking any astrology functions.

Direct and Relevant Responses:
Provide a direct and relevant response to the user's specific query. Avoid including additional or irrelevant information.

Positive Tone:
Ensure every response is optimistic and encouraging.

Clarity:
Break down astrology concepts into simple, understandable terms.

Action-Oriented:
Structure your response with clear, bullet-pointed advice to make it easy for the user to follow your recommendations.

Use Necessary Functions:
If a question requires multiple functions to ensure a thorough and accurate response, use only the necessary functions to avoid confusion. Do not hesitate to call multiple functions if needed.

Handle Out-of-Scope Questions:
If the question falls outside the scope of available functions, politely inform the user that the current system cannot provide an accurate response and encourage them to ask a different question.

Zodiac Sign or Rashi Queries:
Whenever the user asks about their zodiac sign or rashi, refer to user_details.get("kundali").

Incomplete Partner Details:
If partner details are missing or incomplete, ask a counter-question such as "Please provide your partner's details?" or "Select your partner profile?"

Handle Incorrect Questions:
If the question is outside the scope of the available functions, provide a response indicating that the question cannot be addressed with the available functions without giving additional incorrect information.
Today's date is {current_date}. Tomorrow's date is {next_date}.

Here is the user's question: {user_prompt}.
User's details: Date of birth: {user_details.get('dob')}, Time of birth: {user_details.get('tob')}, Latitude: {user_details.get('lat')}, Longitude: {user_details.get('lon')}, Time zone: {user_details.get('tz')}, Zodiac sign: {user_details.get('kundali')},
lang: {lang}.
    """

    if partner_details:
     full_prompt += f""" 
Partner details: Date of birth: {partner_details.get('dob')}, Time of birth: {partner_details.get('tob')}, Latitude: {partner_details.get('lat')}, Longitude: {partner_details.get('lon')}, Time zone: {partner_details.get('tz')}, Zodiac sign: {partner_details.get('kundali')}.
Language: {lang}.
    """

# Complete the full prompt
    full_prompt += "\nHowever, you need to carefully read the user's question and respond accordingly. If you are uncertain about which function to call, use the 'personal_characteristics' function by default."
    
    print("This is user prompt :",user_prompt)
    print("===========================================================")
    print("This is full prompt:",full_prompt)
    print("===========================================================")

    prediction = multiple_api_callings(full_prompt,personId,lang,partnerId)
    
    def generate():
        stream = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prediction}],
            stream=True
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            #print(content)
            yield content

    # Return a streaming response
    return Response(generate(), content_type='text/plain')
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
     