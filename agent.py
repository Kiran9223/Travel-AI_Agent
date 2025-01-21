import google.generativeai as genai
from tools import getCurrentWeather, getLocation
from prompts import prompt
from secret_key import GEMINI_API_KEY
import re

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

availableFunctions = {
    "getCurrentWeather" : getCurrentWeather, 
    "getLocation" : getLocation
}

## Build an agent that can answer any questions that might require knowledge
## about my current location and current weather at my location.

weather = getCurrentWeather()
location = getLocation()

# print(weather, location)

def agent(query):
    MAX_ITERATIONS = 5
    messages = [
            {
                'role': 'model',
                'parts': prompt,
            },
            {
                'role': 'user',
                'parts': query,
            }
    ]
    chat_input = "Check the message history and do the needful"
    for i in range(MAX_ITERATIONS):
        print("Iteration : ", i)
        chat = model.start_chat(
            history=messages
        )
        response = chat.send_message(chat_input)
        print(response.text)
        messages.append({'role': 'model', 'parts': response.text})
        split_response = response.text.split("\n")
        # print("split_response : ", split_response)
        actionStr=""
        match=""
        for s in split_response:
            match = re.search(r"Action:\s*(.*?):", s)
            if match:
                actionStr = s
                break
        # print("actionStr : ",actionStr)
        # print("match : ",match.group(1))
        action = ""
        if match:
            action = match.group(1)
            if action not in availableFunctions:
                print("Action not available : ", action)
                return
            print("Calling function : ", action)
            function = availableFunctions[action]
            observation = function()
            print(observation)
            messages.append({'role': 'model', 'parts': f"Observation : {str(observation)}"})
            # print(messages)
        else:
            print("Agent finished with task")
            print(response.text) 
            break

    

agent("What is the current weather in my location?")

