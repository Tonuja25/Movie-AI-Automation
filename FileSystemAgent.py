from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("genAi connected")
os.makedirs("./assets", exist_ok=True)
def createFile(content:str) ->str:
    with open("./assets/hello.txt","w+") as file:
        file.write(content)
        file.close()
        return " file save successfully"
def readFile() -> str:
    with open("./assets/hello.txt","r+") as file:
        data = file.read()
        file.close()
        return data
# generate a tools

tools = [{
    "function_declarations":[
    {
        "name":"createFile",
        "description":"created text file and save the text file locally saved successfully",
        "parameters":{
            "type":"object",
            "properties":{
                "content":{
                    "type":"string"
                    }
            },
            "required":["content"]
        }
        
    },
    {
    "name":"readFile",
    "description":"read a text file return the content of user input"
    }

    ]
    

}]
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit","quit"]:
        print("Agent:","Bye Bye!")
        break
    responses = client.models.generate_content(
             model="gemini-3.6-flash",
          
            contents = user_input,
            config ={
                 "temperature": 0,

    "system_instruction": """
    You are an AI File Management Assistant.

    1. If the user asks to create a text file,
       use createFile tool.

    2. If the user asks to read a text file,
       use readFile tool.

    3. If the user asks to create a PDF file,
       use createPDF tool.

    4. If the user asks to read a PDF file,
       use readPDF tool.

    5. If the user asks to create an Excel file,
       use createExcel tool.

    6. If the user asks to read an Excel file,
       use readExcel tool.

    7. Always use the appropriate tool for file operations.

    8. After executing the tool, return the result
       to the user.

    9. Never claim a file was created or saved
       unless the tool execution is successful.
    """,
    "tools": tools
}
        )
    msg = responses.candidates[0].content.parts[0].function_call
    if msg:
            tool_name = msg.name
            tool_args = dict(msg.args)
            if tool_name == "createFile":
                        result = createFile(tool_args['content'])
            elif tool_name == "readFile":
                        result = readFile()
            print("Agent:", result)
else:
    print("Agent:", responses.text)
       
  
    



    
    

