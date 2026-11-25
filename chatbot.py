from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    user_input = input("You:")
    if user_input.lower() == "exit":
        print("Agent: Bye Bye!")
        exit(0)
    else:
        response = client.responses.create(
            instructions="-you are an ai assistant when user asked question you give answers or asstant give response i dont know answers",
            model= "gpt-4.1-mini",
            temperature= 0,

            input= user_input
        )
        print("Agent:", response.output_text)