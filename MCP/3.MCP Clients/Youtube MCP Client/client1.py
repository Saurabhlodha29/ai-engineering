import json
import asyncio
from dotenv import load_dotenv

from langchain.mcp import MCPAdapter
from langchain_core.messages import ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()


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
            "url": "https://receive-gbp-ontario-finding.trycloudflare.com/mcp"
        },
        "manim-server": {
            "command": "C:/Users/saura/AppData/Local/Programs/Python/Python311/python.exe",
            "args": [
                "C:/Users/saura/Desktop/manim-mcp-server/src/manim_server.py"
            ],
            "env": {
                "MANIM_EXECUTABLE": "C:/Users/saura/AppData/Local/Programs/Python/Python311/Scripts/manim.exe"
            }
        }
    }
}


async def main() -> None:
    async with MCPAdapter(SERVERS) as adapter:

        # Discover MCP tools and convert them to LangChain tools
        tools = await adapter.list_tools()

        llm = ChatNVIDIA(
            model="nvidia/nemotron-3.5-lightning-30b-a3b"
        )

        llm_with_tools = llm.bind_tools(tools)
        
        named_tools = {}
        
        for tool in tools:
            named_tools[tool.name] = tool
            
        print("\n Available tools : ", named_tools.keys())
        
        # prompt = "What is the product of numbers 238 and 493? Use a tool from the available tools."
        # prompt = "Add an expense for rupees 800 for groceries on 3rd september."
        
        prompt = "Draw a triangle rotating in place using the manim tool."

        response = await llm_with_tools.ainvoke(prompt)
        
        if not getattr(response, "tool_calls", None):
            print(f"\n LLM reply : {response.content}")
            return

        tool_messages = []
        
        for tc in response.tool_calls:
            selected_tool = tc["name"]
            selected_tool_args = tc.get("args") or {}
            selected_tool_id = tc["id"]

            # print(f"Selected tool: {selected_tool}")
            # print(f"Selected tool args: {selected_tool_args}")
            
            result = await named_tools[selected_tool].ainvoke(selected_tool_args)
            # print(f"Tool result : {tool_result}")
            
            tool_messages.append(ToolMessage(content = json.dumps(result), tool_call_id = selected_tool_id))   
        
        final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
        print(f"Final response : {final_response.content}")


if __name__ == "__main__":
    asyncio.run(main())