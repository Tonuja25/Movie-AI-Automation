import streamlit as st
import os
import asyncio

from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

from crud import *

load_dotenv()

st.set_page_config(
    page_title="Movie AI Agent",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie AI Automation System")
st.caption("Manage Movies, Multiplex and Hall Details with Gemini AI")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

config = LocalAgentConfig(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.5-flash-lite",
    tools=[
        saveMovie,
        getAllMovies,
        getMovieById,
        updateMovie,
        deleteMovie,
        saveMultiplex,
        getAllMultiplex,
        saveHall,
        getAllHalls,
        getMovieMultiplex
    ]
)

available_tool: dict = {
    "saveMovie": saveMovie,
    "getAllMovies": getAllMovies,
    "getMovieById": getMovieById,
    "updateMovie": updateMovie,
    "deleteMovie": deleteMovie,
    "saveMultiplex": saveMultiplex,
    "getAllMultiplex": getAllMultiplex,
    "saveHall": saveHall,
    "getAllHalls": getAllHalls,
    "getMovieMultiplex": getMovieMultiplex
}

user_input = st.chat_input("Ask About Movies Hall or multiplex")


async def callAgent():
    async with Agent(config) as agent:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        if user_input.lower() == "exit":
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Bye Bye"
            })
            return

        response = await agent.chat(user_input)

        async for tool in response.tool_calls:
            toolArgs = dict(tool.args)
            toolFunction = available_tool.get(tool.name)
            if toolFunction:
                result = toolFunction(**toolArgs)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": str(result)
                })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Tool Not Found"
                })


if user_input:
    asyncio.run(callAgent())

# History shudhu ekbar, shob shesh-e
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])