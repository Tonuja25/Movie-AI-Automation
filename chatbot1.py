import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
    
)

print("OpenAI connected")
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
    "role": "system",
    "content": "-you want to assistant in medical details and it give all details in medical names and give me medicine prices when ai  don't know answer ai tells  sorry i dont know"
    })
messages = st.session_state.messages
st.title("Medical Detils")
for msg in messages:
    if msg["role"] == "user":
        st.write("You:",msg["content"])
    elif msg["role"] == "assistant":
        st.write("Agent:", msg["content"])

text_obj = st.text_area("Ask Question")
btnClick = st.button("Submit query")
if btnClick:
    st.write("Hello button clicked")
    messages.append({
        "role": "user",
        "content": text_obj

    })
    responses = client.chat.completions.create(
    model = "gpt-4.1-mini",
    temperature = 0,
     messages = messages,
   
    )
    msg = responses.choices[0].message.content
    messages.append({
        "role":"assistant",
        "content":msg
    })
    st.write("Agent Reply:", msg)