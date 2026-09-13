import os
import json
import random
from mcp.server import MCPServer

mcp = MCPServer(name = "Simple Calculator Server")

# Tool: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Tool: Generate a random number
@mcp.tool()
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random number within a specified range."""
    return random.randint(min_val, max_val)

# Resource: Server information
@mcp.resource("info://server")
def server_info() -> str:
    """Get descriptive information about this server."""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "Exposing network tools over an async ASGI layout."
    }

    return json.dumps(info, indent=2)

# Running the server
if __name__ == "__main__":
    # The modern SDK handles network listening directly inside mcp.run()!
    # 'host="0.0.0.0"' allows connections from the public web interface.
    mcp.run(
        transport="sse", 
        host="0.0.0.0", 
        port=10000
    )