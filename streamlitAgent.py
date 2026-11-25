import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import ToolCallExecutionEvent
from tool import *
load_dotenv()
st.set_page_config(
    page_title= "Math & File Agent",
    page_icon= "",
    layout= "centered"
)
st.title("Math & File Agent")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
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
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])
user_input = st.chat_input("Ask About question:")
async def callAgent():
   
        
        if user_input:
            
            if user_input.lower() == "exit":
                st.write("Agent: Bye Bye!")
                return
            else:
                with st.spinner("Agent is Thinking..."):
                   
                    result = await mathorFileAgent.run(
            task = user_input
        )
                    for message in result.messages:
        
                        if isinstance(message,ToolCallExecutionEvent):
                            for tool in message.content:
                                st.write("Agent is using tool:", tool.name)
        msg = result.messages[-1].content
        return msg
                        
if user_input:
    st.session_state.chat_history.append({
                    "role":"user",
                    "content":user_input
                })
    response = asyncio.run(callAgent())
    st.session_state.chat_history.append({
                        "role":"assistant",
                        "content":response
                    })
    st.rerun()
    st.write("Agent:", response)

           