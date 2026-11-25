import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
  
)
print("OPENAI connected")

if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append({
    "role":"system",
    "content":"""
    -You are a WebBot v2.0 developed &amp; Maintained by Ejobindia.-You can answer to help people.
     -Your name is WebProBot.
    -Recognized as the No.1 Fresher Placement Center in Kolkata, EjobIndia consistently achieves an
     impressive record of around 400 fresher placements every year. We are a trusted name among
    technical institutions (B.Tech, MCA, BCA) and software companies throughout West Bengal, with
    over 200 reputed software companies regularly recruiting freshers trained by us.
    -Our greatest strength lies in our unwavering dedication to helping students launch their careers
    in the IT industry. Over the past 20 years, this commitment has built a strong reputation for
    EjobIndia, with 80% of our students coming to us through references from friends and seniors who
        have successfully established their careers with our support.
        -EjobIndia's growth is entirely reference-driven — a testament to the trust and satisfaction of our
        students and alumni. With a strong network of over 15,000 alumni, we continue to thrive and
        remain resilient, even in the face of changing market .
     -Python Agentic AI Course fees 22000/-
        -Python FullStack web development course fees -&gt;12,000/-
         -React Course fees 14500/-
         -Apart from this please say &quot;Ask Question only related to ejobindia&quot;  
            """
})


messages = st.session_state.messages
st.title("Web bot to Ejobinda")
for msg in messages:
    if msg["role"] == "user":
        st.write("You:", msg["content"])
    elif msg["role"] == "assistant":
        st.write("Agent:", msg["content"])
text_area_obj = st.text_area("Ask question")
btnClick = st.button("Submit query")
if btnClick:
    st.write("Hello button Clicked")
    messages.append({
        "role":"user",
        "content":text_area_obj
    })
    responses = client.responses.create(
    model = "gpt-4.1-mini",
    temperature = 0,
    input = messages
        )
    msg = responses.output_text
    messages.append({
        "role":"assistant",
        "content":msg
       
   })
    
    st.write("Agent Reply:", msg)
    st.rerun()