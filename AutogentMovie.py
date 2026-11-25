import streamlit as st
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from crud import *
load_dotenv()
st.set_page_config(
    page_title= "Movie AI Agent",
     page_icon="🎬",
     layout= "centered"
)
st.title("Movie AI Automation system")
st.caption("Manage Multiple movies and  multiplex ,hall detail with openai")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask About movies multiplex or hall")
async def callAgent(question: str) -> str:
    model_client  = OpenAIChatCompletionClient(
    model = "gpt-4.1-mini",
    api_key= os.getenv("OPENAI_API_KEY")
    )
    agent = AssistantAgent(
        name = "movie_agent",
        model_client= model_client,
        tools = [
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
        ],
        system_message= """

            You are a Movie AI Automation Assistant.

            You manage Movies, Multiplex and Hall details
            using the available database tools.

            Your responsibilities:

            1. Add new movie details.
            2. Show all movies.
            3. Find movie details by movie ID.
            4. Update movie details.
            5. Delete movie details.
            6. Add multiplex details.
            7. Show all multiplexes.
            8. Add hall details.
            9. Show all halls.
            10. Show movies by multiplex and hall details.

            Always use the appropriate tools for database operations.

            Never invent database records.

            Ask the user for missing information before
            performing an operation.

            Give simple and clear responses.
"""
    )
    
    result = await agent.run(task=question)
    return str(result.messages[-1].content)

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking"):
            response = asyncio.run(callAgent(user_input))
            st.write(response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
