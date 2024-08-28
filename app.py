from flask import Flask, request,jsonify
from dotenv import load_dotenv
import os
import openai
from utils import multiple_api_callings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = 'gpt-4o-mini'

app = Flask(__name__)

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
User's details: Date of birth: {user_details.get('dob')}, Time of birth: {user_details.get('tob')}, Latitude: {user_details.get('lat')}, Longitude: {user_details.get('lon')}, Time zone: {user_details.get('tz')}, Zodiac sign: {user_details.get('kundali')},
lang: {lang}.

If you are uncertain about which function to call, use the 'personal_characteristics' function by default.
    """

    prediction = multiple_api_callings(full_prompt,personId,lang)

    response = {
        "personId": personId,
        "prediction": prediction
    }

    def generate():
            stream = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": full_prompt}],
                stream=True
            ) 

            for chunk in stream:
                #if chunk.choices[0].delta.content is not None:
                delta_content = getattr(chunk.choices[0].delta, 'content', None)
                if delta_content:
                      yield delta_content
                   
    return generate(), {"Content-Type": "text/plain"}


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
     