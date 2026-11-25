from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
import json
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def encode_image(image_path):
    with open(image_path, "rb") as imagepath:
        return base64.b64encode(imagepath.read()).decode("utf-8")
image_path = "./Agent/image/invoice.jpg"
base64_image = encode_image(image_path= image_path)
while True:
        user_input = input("You:")
        if user_input.lower() in ["exit","quit"]:
            print("Agent: Bye Bye!")
            exit(0)
    
        response = client.chat.completions.create(
             model = "gpt-4.1-mini",
             temperature= 0,
           
messages=[
    {
        "role": "system",
        "content": "- You are an image analyzer. Analyze the image, extract text inside the image, and summarize the image. For other topics say: Sorry, I can only analyze images."
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }
        
]
        )
        

        result = response.choices[0].message.content
        print("Agent:", result)