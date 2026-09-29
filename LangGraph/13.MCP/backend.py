import asyncio
import requests
import aiosqlite

from typing import TypedDict, Annotated
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from mcp_manager import get_mcp_tools, run_async


load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


# ============================================================
# Normal tools
# ============================================================

search_tool = DuckDuckGoSearchRun(region="us-en")


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Get the current stock price for a given stock symbol.
    """

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey=C9PE94QUEW9VWGFM"
    )

    response = requests.get(url)

    return response.json()


# ============================================================
# MCP tools
# ============================================================

mcp_tools = get_mcp_tools()


# ============================================================
# All tools
# ============================================================

tools: list[BaseTool] = [
    search_tool,
    get_stock_price,
    *mcp_tools,
]


# ============================================================
# LLM with tools
# ============================================================

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# State
# ============================================================

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ============================================================
# ASYNC CHAT NODE
# ============================================================

async def chat_node_async(state: ChatState):
    """
    Actual asynchronous LLM call.

    This is the real async implementation.
    """

    messages = state["messages"]

    response = await llm_with_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


# ============================================================
# SYNC BRIDGE FOR STREAMLIT / LANGGRAPH
# ============================================================

def chat_node(state: ChatState):
    """
    Synchronous wrapper around the asynchronous chat node.

    Streamlit uses chatbot.stream(), so LangGraph expects
    a synchronous node here.

    The actual LLM call still runs asynchronously on the
    dedicated MCP event loop.
    """

    return run_async(
        chat_node_async(state)
    )


# ============================================================
# TOOL NODE
# ============================================================

tool_node_async = ToolNode(tools)


async def run_tool_node_async(state: ChatState):
    """
    Execute tools asynchronously.

    This is important because MCPAdapter tools are async.
    """

    return await tool_node_async.ainvoke(state)


def tool_node(state: ChatState):
    """
    Synchronous bridge for the asynchronous ToolNode.

    frontend.py can therefore continue using:

        chatbot.stream(...)

    while MCP tools are executed using:

        await tool_node_async.ainvoke(...)
    """

    return run_async(
        run_tool_node_async(state)
    )


# ============================================================
# BUILD GRAPH
# ============================================================

graph = StateGraph(ChatState)


graph.add_node(
    "chatbot",
    chat_node
)

graph.add_node(
    "tools",
    tool_node
)


# ============================================================
# EDGES
# ============================================================

graph.add_edge(
    START,
    "chatbot"
)


graph.add_conditional_edges(
    "chatbot",
    tools_condition
)


graph.add_edge(
    "tools",
    "chatbot"
)


# ============================================================
# CHECKPOINTER
# ============================================================

async def init_checkpointer():
    """
    Create the asynchronous SQLite checkpointer.
    """

    conn = await aiosqlite.connect(
        "chatbot.db"
    )

    checkpointer = AsyncSqliteSaver(conn)

    await checkpointer.setup()

    return checkpointer


checkpointer = run_async(
    init_checkpointer()
)


# ============================================================
# COMPILE GRAPH
# ============================================================

chatbot = graph.compile(
    checkpointer=checkpointer
)


# ============================================================
# THREAD MANAGEMENT
# ============================================================

async def _alist_threads():

    all_threads = set()

    async for checkpoint in checkpointer.alist(None):

        thread_id = (
            checkpoint.config
            .get("configurable", {})
            .get("thread_id")
        )

        if thread_id:
            all_threads.add(thread_id)

    return list(all_threads)


def retrieve_all_threads():

    return run_async(
        _alist_threads()
    )