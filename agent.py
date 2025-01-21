import google.generativeai as genai
from tools import getCurrentWeather, getLocation
from prompts import prompt
from secret_key import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

## Build an agent that can answer any questions that might require knowledge
## about my current location and current weather at my location.

weather = getCurrentWeather()
location = getLocation()

# print(weather, location)

def agent(query):
    chat = model.start_chat(
        history=[
            {
                'role': 'model',
                'parts': prompt,
            },
            {
                'role': 'user',
                'parts': query,
            }
        ]
    )
    response = chat.send_message(query)
    print(response.text)

agent("Please give me some ideas for activities to do this afternoon.")

