import smtplib 
#smtplib - simple mail transfer libary
from email.mime.text import MIMEText 
# python ar akta module ba class text message tairi kora (Multipurpose internet mail extension)
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import json
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
def email_send(body:str, subject:str, receiver:str) -> str:
    Sender = os.getenv("EMAIL_ID")
    sender_pass = os.getenv("EMAIL_PASSWORD")
    if not Sender or not sender_pass:
        return "Email or password not configured!"
   
    message = MIMEText(body)
    message['subject'] = subject
    message['from'] = Sender
    message["to"] = receiver
    try:
        with smtplib.SMTP('smtp.gmail.com',587) as server:
        
            server.starttls() 
            # এর কাজ হলো Email server-এর সঙ্গে secure encrypted connection তৈরি করা।
            server.login(Sender,sender_pass)
            server.send_message(message)
            return "Send Message Successfully"
    except Exception as ex:
                print("SMTP Error:", ex)
                return "Email sending failed!"
# create a tool
tools = [{
            "type":"function",
            "function":{
                "name":"email_send",
                 "description":"This tool is used to send email, from user prompt take the mail subject , body and reciver email id. Use this tool whenever user say create a content based on the topic and sent to reciver email id.",
                 "parameters":{
                     "type":"object",
                     "properties":{
                                            "receiver":{
                                                "type":"string",
                                                
                                            },
                                            "subject":{
                                                "type":"string",
                                            },
                                            "body":{
                                                "type":"string"
                                            },
                   
                                        }
                 },
                 "required":["receiver","subject", "body"]
            }
        }]

    
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        print("Agent:","Bye!")
        exit(0)
    response = client.chat.completions.create(
            model = "gpt-4.1-mini",
       
        messages = [{
            "role":"system",
    "content": "- You are an email sending agent. Your name is Tonuja Dey Sarkar. You will create the email content and send the email to the receiver's email ID. Extract the receiver's email ID, email subject, and email body from the user's prompt. Always end every generated email body with 'Best Regards,\nTonuja Dey Sarkar'. Whenever someone asks about any other topic, reply: I can only help with sending emails."
        },
        {
            'role':"user",
            "content": user_input
        }
       
        ],
         tools = tools
         )
    result = response.choices[0].message
    if result.tool_calls:
                tool_name = result.tool_calls[0].function.name
                tool_arg =json.loads(result.tool_calls[0].function.arguments)
                if tool_name == "email_send":
                   SendMail = email_send(
                    tool_arg["body"],
                    tool_arg["subject"],
                    tool_arg["receiver"]
                    )
                   print("Agent:",  SendMail)
    else:
            print("Agent: Error!")
  
    
    