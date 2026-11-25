# user input -> llm -> decide tools -> tools yes - > tool call -> python execute function -> return result -> final answer -> user sees output

from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def calculate(a:int, b:int, operation:str):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a-b
    elif operation == "multiply":
        return a * b
    elif operation == "division":
        if  b == 0:
            return 'cannot divide by zero'
        return a / b
    elif operation == "modulo":
        if b == 0:
            return 'cannot divide by zero'
        return  a % b
    else:
        return "Invalid Operation"
# create a tool
tools = [{
    "type":"function",
    "function":{
        "name":"addNumbers",
       "description": """
You are a mathematical calculation tool designed to perform
accurate arithmetic operations on two integer numbers.

This function accepts three parameters:
- a: The first integer number.
- b: The second integer number.
- operation: The mathematical operation requested by the user.

Supported mathematical operations:

1. Addition (add): Adds two numbers and returns their sum.
2. Subtraction (subtract): Subtracts the second number from the first number.
3. Multiplication (multiply): Multiplies two numbers and returns the product.
4. Division (division): Divides the first number by the second number.
5. Modulo (modulo): Returns the remainder after dividing the first number by the second number.

Instructions:
- Select the correct operation based on the user's request.
- Pass both numbers as integer arguments.
- Always use the appropriate operation.
- Do not perform division or modulo when the second number is zero.
- Return the calculated result accurately.
""",
            "parameters":{
        "type":"object",
        "properties":{
            "a":{
            "type":"integer",
            "description":"It is a numeric value convert integer"
            },
            "b":{
                "type":"integer",
                "description":"It is a numeric value convert integer"
            },
              "operation":{
                    "type":"string",
                        "enum": ["add", "subtract", "multiply", "division", "modulo"],
                        "description":"Select Mthematical operation"
                },
            
        
        },
          "required":["a","b","operation"]
     
    },
    },
  
}]

while True:
    user_input = input("You:")
    if user_input.lower() in ["exit",'quit']:
        print("Agent:", "Bye Bye")
        exit(0)
    else:
        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            temperature = 0,
            
        
        messages = [{
            'role':"user",
            "content":user_input,
           
        }
        ],
        tools = tools
        )
        msg = response.choices[0].message
        if msg.tool_calls:
            tool_name = msg.tool_calls[0].function.name
            tool_args = json.loads(msg.tool_calls[0].function.arguments)
            if tool_name == "addNumbers":
              result = calculate(
                  tool_args["a"], 
                  tool_args["b"],tool_args["operation"])
            print("Agent:", result)
        else:
            print(msg.content)

        