import json
import asyncio
import streamlit as st

from dotenv import load_dotenv
from langchain.mcp import MCPAdapter
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
)
from langchain_nvidia_ai_endpoints import ChatNVIDIA


load_dotenv()


# ============================================================
# MCP SERVER CONFIGURATION
# ============================================================

SERVERS = {
    "mcpServers": {
        "math": {
            "command": "C:/Users/saura/.local/bin/uv.exe",
            "args": [
                "run",
                "mcp",
                "run",
                "C:/Users/saura/OneDrive/Desktop/AI Engineering/MCP/3.MCP Clients/Local Server/main.py",
            ],
        },

        "expense": {
            "transport": "streamable-http",
            "url": "https://receive-gbp-ontario-finding.trycloudflare.com/mcp",
        },

        "manim-server": {
            "command": "C:/Users/saura/AppData/Local/Programs/Python/Python311/python.exe",
            "args": [
                "C:/Users/saura/Desktop/manim-mcp-server/src/manim_server.py"
            ],
            "env": {
                "MANIM_EXECUTABLE": (
                    "C:/Users/saura/AppData/Local/Programs/"
                    "Python/Python311/Scripts/manim.exe"
                )
            },
        },
    }
}


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = (
    "You have access to tools. "
    "When you choose to call a tool, do not narrate status updates. "
    "After tools run, return only a concise final answer."
)


# ============================================================
# ASYNC MCP + LLM LOGIC
# ============================================================

async def process_message(history):

    # MCPAdapter manages the MCP connections
    async with MCPAdapter(SERVERS) as adapter:

        # ----------------------------------------------------
        # 1. Get MCP tools and convert them to LangChain tools
        # ----------------------------------------------------

        tools = await adapter.list_tools()

        tool_by_name = {
            tool.name: tool
            for tool in tools
        }

        # ----------------------------------------------------
        # 2. Create LLM
        # ----------------------------------------------------

        llm = ChatNVIDIA(
            model="nvidia/nemotron-3.5-lightning-30b-a3b"
        )

        # Give MCP tools to the LLM
        llm_with_tools = llm.bind_tools(tools)

        # ----------------------------------------------------
        # 3. First LLM call
        # ----------------------------------------------------

        first_response = await llm_with_tools.ainvoke(history)

        tool_calls = getattr(first_response, "tool_calls", None)

        # ----------------------------------------------------
        # 4. No tool required
        # ----------------------------------------------------

        if not tool_calls:

            history.append(first_response)

            return first_response.content


        # ----------------------------------------------------
        # 5. LLM requested one or more tools
        # ----------------------------------------------------

        # IMPORTANT:
        # The assistant message containing tool_calls
        # must come before ToolMessages.

        history.append(first_response)

        tool_messages = []

        for tool_call in tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call.get("args") or {}
            tool_call_id = tool_call["id"]

            # Sometimes arguments can arrive as a JSON string
            if isinstance(tool_args, str):
                try:
                    tool_args = json.loads(tool_args)
                except json.JSONDecodeError:
                    pass

            # Find the requested LangChain tool
            tool = tool_by_name[tool_name]

            # Execute MCP tool
            result = await tool.ainvoke(tool_args)

            # Send result back as ToolMessage
            tool_messages.append(
                ToolMessage(
                    content=json.dumps(result, default=str),
                    tool_call_id=tool_call_id,
                )
            )

        # Add all tool results to conversation history
        history.extend(tool_messages)

        # ----------------------------------------------------
        # 6. Final LLM call
        # ----------------------------------------------------

        final_response = await llm_with_tools.ainvoke(history)

        history.append(
            AIMessage(
                content=final_response.content or ""
            )
        )

        return final_response.content or ""


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="MCP Chat",
    page_icon="🧰",
    layout="centered",
)

st.title("🧰 MCP Chat")


# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================

if "history" not in st.session_state:

    st.session_state.history = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]


# ============================================================
# RENDER PREVIOUS CHAT
# ============================================================

for message in st.session_state.history:

    if isinstance(message, SystemMessage):
        continue

    elif isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        # Don't display intermediate AI tool-call messages
        if getattr(message, "tool_calls", None):
            continue

        with st.chat_message("assistant"):
            st.markdown(message.content or "")

    # ToolMessages intentionally aren't rendered


# ============================================================
# CHAT INPUT
# ============================================================

user_text = st.chat_input("Type a message...")


if user_text:

    # --------------------------------------------------------
    # Display user message immediately
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(user_text)

    # Add user message to history
    st.session_state.history.append(
        HumanMessage(content=user_text)
    )

    # --------------------------------------------------------
    # Run MCP + LLM logic
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            final_answer = asyncio.run(
                process_message(st.session_state.history)
            )

        st.markdown(final_answer)