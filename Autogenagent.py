from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
load_dotenv()
from tool import *
from autogen_agentchat.messages import ToolCallExecutionEvent
import asyncio
client = OpenAIChatCompletionClient(
    api_key= os.getenv("OPENAI_API_KEY"),
    model= "gpt-4.1-mini",
    temperature=1
)
print("OpenAI connected")
mathorFileAgent = AssistantAgent(
    name = "MathAgent_FileAgent",
    model_client= client,
    tools=[addNumbers,MultiplyNumbers,subtractNumbers,saveFile,readFile,clientIP,getCurrentTime],
    system_message= """-you are an agent please Create a math agent and create Ip address and datetime mathamatical agent addition , multiplication, subtraction, and save the file and read file hello.text and create a exact ip address and date. 
    when you don't know the content Agent tell sorry i don't know.

"""
)
async def callAgent():
    while True:
        user_input = input("You:")
        if user_input.lower() == "exit":
            print("Agent: Bye Bye!")
            return
        result = await mathorFileAgent.run(
            task = user_input
        )
        for message in result.messages:
              if isinstance(message,ToolCallExecutionEvent):
                                    for tool in message.content:
                                        print("Agent is using tool:", tool.name)
                                        # print("Tool Arguments:", tool.schema_json)
        msg = result.messages[-1].content
        print("Agent:", msg)
if __name__ == "__main__":
    asyncio.run(callAgent())
                                       
                  
   
       
          