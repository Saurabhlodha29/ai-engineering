from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import sqlite3

load_dotenv()

model = ChatNVIDIA(model = "openai/gpt-oss-20b")

# Define State
class MessageState(TypedDict):  
    messages : Annotated[list[BaseMessage], add_messages]
    
    
# Define Chatbot function
def chat_node(state : MessageState):
    messages = state['messages']
    
    response = model.invoke(messages).content
    
    return {'messages':[response]}

    
# Define Graph
graph = StateGraph(MessageState)

# Nodes & Edges
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


# Creating Database
conn = sqlite3.connect(database = 'chatbot.db',check_same_thread = False)

# Checkpointer
checkpointer = SqliteSaver(conn = conn)

chatbot = graph.compile(checkpointer = checkpointer)

# Extracting all the threads from the database

def retrieve_all_threads():
    all_threads = set()
    
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)


# Testing the database : 

# CONFIG = {'configurable':{'thread_id':'thread-1'}}

# response = chatbot.invoke(
#                 {'messages':[HumanMessage(content = "Hi my name is Saurabh")]},
#                 config = CONFIG
#             )

# print(response)