import asyncio
import threading
from langchain.mcp import MCPAdapter


# ============================================================
# MCP Server Configuration
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

expense_api_key = os.getenv("ZOHO_API_KEY")


SERVERS = {
    "mcpServers": {

        # ----------------------------------------------------
        # Local Arithmetic MCP Server
        # ----------------------------------------------------
        "arith": {
            "command": "C:/Users/saura/.local/bin/uv.exe",
            "args": [
                "run",
                "mcp",
                "run",
                "C:/Users/saura/OneDrive/Desktop/AI Engineering/MCP/3.MCP Clients/Local Server/main.py",
            ],
        },

        # ----------------------------------------------------
        # Zoho Expense MCP Server
        # ----------------------------------------------------
        "expense": {
            "command": "npx",
            "args": [
                "mcp-remote",
                f"https://my-server-60088201122.zohomcp.in/mcp/{expense_api_key}/message",
                "--transport",
                "http-only"
            ]
        }
    }
}


# ============================================================
# Dedicated MCP Async Event Loop
# ============================================================

_ASYNC_LOOP = asyncio.new_event_loop()

_ASYNC_THREAD = threading.Thread(
    target=_ASYNC_LOOP.run_forever,
    daemon=True
)

_ASYNC_THREAD.start()


def run_async(coro):
    """
    Run an async coroutine on the dedicated MCP event loop
    and wait for its result.
    """
    future = asyncio.run_coroutine_threadsafe(
        coro,
        _ASYNC_LOOP
    )

    return future.result()


def submit_async_task(coro):
    """
    Submit an async task to the MCP event loop without
    blocking the caller.
    """
    return asyncio.run_coroutine_threadsafe(
        coro,
        _ASYNC_LOOP
    )


# ============================================================
# Persistent MCP Adapter
# ============================================================

_adapter = None
_mcp_tools = None


def _strip_server_prefix(tools):
    """
    MCPAdapter (FastMCP) namespaces every tool as '{server}_{tool}',
    e.g. 'expense_add_expense'. The LLM (Groq / gpt-oss) tends to call
    the tool by its real MCP name ('add_expense'), and Groq rejects any
    call whose name is not in request.tools.

    So we restore the original names, but only when that is safe
    (i.e. the stripped name is unique across all tools and does not
    clash with the non-MCP tools).
    """

    reserved = {"duckduckgo_search", "get_stock_price"}
    prefixes = tuple(f"{name}_" for name in SERVERS["mcpServers"])

    def stripped(name):
        for prefix in prefixes:
            if name.startswith(prefix):
                return name[len(prefix):]
        return name

    candidates = [stripped(t.name) for t in tools]

    for tool, new_name in zip(tools, candidates):
        if (
            new_name != tool.name
            and candidates.count(new_name) == 1
            and new_name not in reserved
        ):
            tool.name = new_name

    return tools


async def _start_mcp():
    """
    Start MCPAdapter and keep its context alive permanently.
    """

    global _adapter, _mcp_tools

    _adapter = MCPAdapter(SERVERS)

    await _adapter.__aenter__()

    _mcp_tools = _strip_server_prefix(await _adapter.list_tools())

    print(
        f"MCPAdapter started. Loaded {len(_mcp_tools)} tools: "
        f"{[t.name for t in _mcp_tools]}"
    )

    # Keep the adapter context alive forever.
    await asyncio.Event().wait()


def start_mcp():
    """
    Start the persistent MCPAdapter in the background.
    """

    future = asyncio.run_coroutine_threadsafe(
        _start_mcp(),
        _ASYNC_LOOP
    )

    # Wait until the adapter has actually loaded its tools.
    while _mcp_tools is None:
        import time
        time.sleep(0.05)

    return future


def get_mcp_tools():
    """
    Return the MCP tools loaded by the persistent adapter.
    """

    if _mcp_tools is None:
        raise RuntimeError(
            "MCPAdapter has not been started yet."
        )

    return _mcp_tools


# ============================================================
# Start MCP when this module is imported
# ============================================================

start_mcp()