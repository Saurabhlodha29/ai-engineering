import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Define config
CONFIG = {'configurable':{'thread_id':'thread_1'}}


# st.session_state -> dict
if 'message_history' not in st.session_state:
    
    # Define message history in the format = [{'role':'...','content':'..'}]
    st.session_state['message_history'] = []


# Showing the whole message history before showing the current messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


# Input box
user_input = st.chat_input('Type here')

if user_input:
    
    # Add the message to message history first
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
    with st.chat_message('user'):
        st.text(user_input)
        
    # The question first goes to LLM
    response = chatbot.invoke({'messages':[HumanMessage(user_input)]},config = CONFIG)
    ai_message = response['messages'][-1].content
    
    # Add the message to message history first
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    
    with st.chat_message('assistant'):
        st.text(ai_message)