from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import json
from fpdf import FPDF
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def createPDF(content:str) -> str:
 pdf = FPDF()
 pdf.add_page()
 pdf.set_font("Arial", size = 12)
 pdf.multi_cell(0,10, content)
 pdf.output("./test.pdf")
 return "PDF created successfully"
def readPDF() -> str:
    pdfReader = PdfReader("./test.pdf")
    pdfContent = ""
    for page in pdfReader.pages:
        pdfContent += page.extract_text()
    return pdfContent
    

 



# create tools
tools = [{
 "type":"function",
 "function":{
  "name":"createPDF",
  "description":"create a test.pdf and save file in local system",
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
         "name": "readPDF",
         "description":"read the file to user content to the user"
     }
 }
]
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        print("Thank you for visiting!")
        exit(0)
    responses = client.chat.completions.create(
        model = "gpt-4.1-mini",
       
        
    messages = [{
            "role":"system",
       "content": """
You are an Agentic AI PDF assistant.
When the user asks to create a PDF with questions and answers,
generate the complete questions and answers.
Then call createPDF and pass the generated content.
When the user asks to read the PDF, call readPDF.
"""
        },
        {
            "role":"user",
            "content":user_input
        }
        ],
    tools=tools
    )
   
    msg  = responses.choices[0].message
    if msg.tool_calls:
            tool_name = msg.tool_calls[0].function.name
            tool_args = json.loads(msg.tool_calls[0].function.arguments)
            if tool_name == "createPDF":
                output = createPDF(tool_args["content"])
            elif tool_name == "readPDF":
                output = readPDF()
            print("Agent:", output)
    else:
            print("Agent: I can only help pdf to create and read file to content!")
