from openai import OpenAI
from dotenv import load_dotenv
from openpyxl import workbook,load_workbook
import json
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def createExcel(content:str) -> str:
    wb =  workbook.Workbook()
    ws = wb.active
    ws.title = "question answer"
    ws.append([content])
    wb.save("./test1.xlsx")
    return "excel created successfully"
def readExcel() -> str:
    wb = load_workbook("./test1.xlsx")
    ws = wb.active
    excelContent = ""
    for page in ws.iter_rows(values_only=True):
            excelContent += str(page)
    return excelContent
    

tools = [{
 "type":"function",
 "function":{
  "name":"createExcel",
  "description":"create a test1.excel and save file in local system",
  "parameters":{
    "type":"object",
    "properties":{
     "content":{
      "type":"string"
     }
      
    },
       "required": ["content"]

  }
  


 }

 
   

},
 {
     "type":"function",
     "function":{
         "name": "readExcel",
         "description":"read the file to user content to the user"
     }
 }
]
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit","quit"]:
        print("Agent:", "   Thankyou For Visiting")
        exit(0)
    responses = client.chat.completions.create(
            model = "gpt-4.1-mini",
        
        messages = [{
            "role":"system",
                   "content": """
You are an Agentic AI Excel assistant.
When the user asks to create a Excel with questions and answers,
generate the complete questions and answers.
Then call createExcel and pass the generated content.
When the user asks to read the PDF, call readExcel.
"""
        },
        {
            "role":"user",
            "content":user_input
        }
        
        ],
    tools = tools
        )
    msg = responses.choices[0].message
    if msg.tool_calls:
            tool_name = msg.tool_calls[0].function.name
            tool_args = json.loads(msg.tool_calls[0].function.arguments)
            if tool_name == "createExcel":
             output = createExcel(tool_args["content"])
             print("Agent:", output)
            elif tool_name == "readExcel":
                output = readExcel()
                print("Agent:",output)
            else:
                 print("Agent: I can only help Excel to create and read file to content!")
    else:
         print("Agent:", msg.content)

        
