import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

print("OpenAi connected")
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
    "role": "system",
    "content": "-It is Ai assitant contentt Please tell me food details price and  famous food in india when ai dont know ai responses sorry i don't know "

})
messages = st.session_state.messages
st.title("Food Order")

for msg in messages:
    if msg["role"] == "user":
        st.write("You:", msg["content"])
    elif msg['role'] == "assistant":
        st.write("Agent:", msg["content"])

text_area_obj = st.text_area("Ask Question")
btnClick = st.button("Submit Query")
if btnClick:
    st.write("Hello Button gtets clicked")
    st.session_state.messages.append({
        "role": "user",
        "content": text_area_obj
    })
    responses = client.chat.completions.create(
        model = "gpt-4.1-mini",
        temperature = 0,
        messages= messages
    )
    msg = responses.choices[0].message.content
    messages.append({
        "role":"assistant",
        "content": msg
    })
   
    st.write("Agent Reply :",msg)