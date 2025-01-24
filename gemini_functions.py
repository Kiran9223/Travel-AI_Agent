from secret_key import GEMINI_API_KEY
import google.generativeai as genai
from tools import tools

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash", tools=tools)

def agent(query):
    messages = [
        {
            'role': 'user',
            'parts': """You are a helpful AI Agent. You will be provided with a set of tools that you can call upon to help the user. 
                        If you are unsure how to respond, please ask clarifying questions. If you do not know the answer, please say that you do not know. """,
        },
        {
            'role': 'user',
            'parts': query,
        }
    ]

    chat = model.start_chat(enable_automatic_function_calling=True, history=messages)

    response = chat.send_message("")

    print(response)


query = "What is my current location and the weather?"
agent(query)