import google.generativeai as genai
from tools import getCurrentWeather, getLocation
from prompts import prompt
from secret_key import GEMINI_API_KEY
import re

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
    #  /**
    #  * PLAN:
    #  * 1. Split the string on the newline character \n
    #  * 2. Search through the array of strings for one that has "Action:"
    #  * 3. Parse the action (function and parameter) from the string
    #  * 4. Calling the function
    #  * 5. Add an "Obversation" message with the results of the function call
    #  */
    split_response = response.text.split("\n")
    actionStr=""
    match=""
    for s in split_response:
        match = re.search(r"Action:\s*(.*?):", s)
        if match:
            actionStr = s
            break
    print(actionStr)
    print(match.group(1))
    
    

agent("Please give me some ideas for activities to do this afternoon.")

