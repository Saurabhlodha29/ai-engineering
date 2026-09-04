from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import sqlite3

import os
import requests
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

load_dotenv()

llm = ChatNVIDIA(model = "nvidia/nemotron-3.5-lightning-30b-a3b")  # This model supports native tool calling in langchain

# -------------------------------------------------
# 1.Tools 
# -------------------------------------------------

search_tool = DuckDuckGoSearchRun(region = 'us-en')

@tool
def calculator(first_num : float, second_num : float, operation : str) -> dict:
    """
    Perform a basic arithematic operation on two numbers,
    supported operations : add, sub, mul, div
    """
    
    try:
        if operation == 'add':
            result = first_num + second_num
        elif operation == 'sub':
            result = first_num - second_num
        elif operation == 'mul':
            result = first_num * second_num
        elif operation == 'div':
            if second_num == 0:
                return {'error':'Division by zero is not allowed!'}
            else:
                result = first_num / second_num
        else:
            return {'error':f'Unsupported operation: {operation}'}
        
        return {'first_num':first_num,'second_num':second_num,'operation':operation,'result':result}
        
    except Exception as e:
        return {'error':str(e)}
    
@tool
def get_stock_price(symbol : str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g, 'AAPL','TSLA')
    Using Alpha Vantage with api key in the url.
    """
    
    api_key = os.environ['STOCK_API_KEY']
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    
    r = requests.get(url)
    return r.json()

    
# Make tools list
tools = [search_tool, calculator, get_stock_price]

# Make LLM tool aware
llm_with_tools = llm.bind_tools(tools)

# -------------------------------------------------
# 2.Define State
# -------------------------------------------------

class MessageState(TypedDict):  
    messages : Annotated[list[BaseMessage], add_messages]

# -------------------------------------------------
# 3.Define Chatbot functions
# -------------------------------------------------

# Chatnode function
def chat_node(state : MessageState):
    """LLM node that may answer a question or request a tool call."""
    messages = state['messages']
    
    response = llm_with_tools.invoke(messages)
    
    return {'messages':[response]}

# Toolnode function
tool_node = ToolNode(tools)   # Execute tool calls

# -------------------------------------------------
# 4.Define Graph
# -------------------------------------------------

graph = StateGraph(MessageState)

# Nodes & Edges
graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START,'chat_node')

# If LLM asks for a tool, go to tool_node, else finish
graph.add_conditional_edges('chat_node',tools_condition)

# Send back the tool response to the LLM to decide whether re-execution is needed or the final output is already acquired
graph.add_edge('tools','chat_node')


# -------------------------------------------------
# 5.Creating Database
# -------------------------------------------------

conn = sqlite3.connect(database = 'chatbot.db',check_same_thread = False)

# -------------------------------------------------
# 6.Checkpointer
# -------------------------------------------------

checkpointer = SqliteSaver(conn = conn)

chatbot = graph.compile(checkpointer = checkpointer)


# -------------------------------------------------
# 7.Helper Function
# -------------------------------------------------

def retrieve_all_threads():
    all_threads = set()
    
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)