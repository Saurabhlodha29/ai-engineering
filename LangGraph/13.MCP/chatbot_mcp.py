from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict, Annotated
from dotenv import load_dotenv

import os
import asyncio
from langchain.mcp import MCPAdapter
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

llm = ChatNVIDIA(model = "nvidia/nemotron-3.5-lightning-30b-a3b")  # This model supports native tool calling in langchain

# -------------------------------------------------
# 1.MCP Server Config
# -------------------------------------------------

api_key = os.getenv("ZOHO_API_KEY")

SERVERS = {
    "mcpServers": {
        "arith": {
            "command": "C:/Users/saura/.local/bin/uv.exe",
            "args": [
                "run",
                "mcp",
                "run",
                # Loation of the local MCP server
                "C:/Users/saura/OneDrive/Desktop/AI Engineering/MCP/3.MCP Clients/Local Server/main.py",
            ],
        },
        # We are using Zoho's MCP server as an expnse tracker MCP Server
        "expense": {
            "command": "npx",
                        "args": [
                                "mcp-remote",
                                f"https://my-server-60088201122.zohomcp.in/mcp/{api_key}/message",
                                "--transport",
                                "http-only"
                        ]
        }
    }
}

# -------------------------------------------------
# 2.Define State
# -------------------------------------------------

class MessageState(TypedDict):  
    messages : Annotated[list[BaseMessage], add_messages]
    
async def build_graph(adapter):
    
    # Use the adapter to fetch tools
    tools = await adapter.list_tools()
    llm_with_tools = llm.bind_tools(tools)
    
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
    
    # Creating the MCP Client
    # Make the adapter available for the entire graph
    async with MCPAdapter(SERVERS) as adapter:
        
        # Build graph using the adapter
        chatbot = await build_graph(adapter)
        
        # Running the graph
        # result = await chatbot.ainvoke({'messages':[HumanMessage(content = 'Find the modulus of 132354 and 23 and give the answer like a cricket commentator.')]})
        
        result = await chatbot.ainvoke({'messages':[HumanMessage(content = 'Add an expense of Rs.500 spent on a Udemy course on Sept-5th-2026.')]})

        print(result['messages'][-1].content)
    
if __name__ == '__main__':
    asyncio.run(main())