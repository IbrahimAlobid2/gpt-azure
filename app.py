import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
azure_api : str =os.getenv("AZURE_OPENAI_API_KEY") 
api_version : str =  os.getenv("API_VERSION")
azure_endpoint : str =  os.getenv("AZURE_OPENAI_ENDPOINT")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Chat with GPT!",
    layout="centered"
)

# Initialize Groq client
client = client = AzureOpenAI(
            api_key=azure_api ,
            api_version = api_version ,
          azure_endpoint=azure_endpoint
        )


# Initialize the chat history in Streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Set the title of the app
st.title(" CHATGPT_4O")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask Me...")

if user_prompt:
    
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable and professional assistant capable of providing expert advice on a wide range of topics. Your expertise spans technology, business, science, health, education, and more. You deliver accurate, concise, and practical answers tailored to the user's specific needs, ensuring clarity, reliability, and professionalism in every response."
        },

        {
            "role": "user",
            "content": user_prompt
        },
    
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
 