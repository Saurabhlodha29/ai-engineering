from __future__ import annotations
from mcp.server import MCPServer

mcp = MCPServer("arith")


def _as_number(x):
    """Convert an int, float, or numeric string into a float."""
    if isinstance(x, (int, float)):
        return float(x)

    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            raise ValueError(f"Invalid numeric value: {x}")

    raise TypeError("Expected a number (int/float or numeric string)")


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Return a + b."""
    return _as_number(a) + _as_number(b)


@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Return a - b."""
    return _as_number(a) - _as_number(b)


@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """Return a * b."""
    return _as_number(a) * _as_number(b)


@mcp.tool()
async def divide(a: float, b: float) -> float:
    """Return a / b."""
    b = _as_number(b)

    if b == 0:
        raise ValueError("Cannot divide by zero")

    return _as_number(a) / b

@mcp.tool()
async def power(a: float, b: float) -> float:
    """Return a ** b."""
    return _as_number(a) ** _as_number(b)

@mcp.tool()
async def modulus(a: float, b: float) -> float:
    """Return a % b."""
    return _as_number(a) % _as_number(b)


if __name__ == "__main__":
    mcp.run()