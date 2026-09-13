from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import sqlite3

import os
import asyncio
import requests
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

load_dotenv()

llm = ChatNVIDIA(model = "nvidia/nemotron-3.5-lightning-30b-a3b")  # This model supports native tool calling in langchain

# -------------------------------------------------
# 1.Tools 
# -------------------------------------------------

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

    
# Make tools list
tools = [calculator]

# Make LLM tool aware
llm_with_tools = llm.bind_tools(tools)

# -------------------------------------------------
# 2.Define State
# -------------------------------------------------

class MessageState(TypedDict):  
    messages : Annotated[list[BaseMessage], add_messages]
    
def build_graph():
    
    # Chatnode function
    async def chat_node(state : MessageState):
        """LLM node that may answer a question or request a tool call."""
        messages = state['messages']
        
        response = await llm_with_tools.ainvoke(messages)
        
        return {'messages':[response]}

    # Toolnode function
    tool_node = ToolNode(tools)

    # Defining Graph
    graph = StateGraph(MessageState)

    # Nodes & Edges
    graph.add_node('chat_node',chat_node)
    graph.add_node('tools',tool_node)

    graph.add_edge(START,'chat_node')
    graph.add_conditional_edges('chat_node',tools_condition)
    graph.add_edge('tools','chat_node')

    # Compile graph
    chatbot = graph.compile()
    
    
    return chatbot

async def main():
    
    chatbot = build_graph()
    
    # Running the graph
    result = await chatbot.ainvoke({'messages':[HumanMessage(content = 'Find the modulus of 132354 and 23 and give the answer like a cricket commentator.')]})

    print(result['messages'][-1].content)
    
if __name__ == '__main__':
    asyncio.run(main())