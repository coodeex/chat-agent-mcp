from mcp.server.fastmcp import FastMCP
from app import get_cat_fact

# Start the MCP server
mcp = FastMCP("cat-facts-mcp")

@mcp.tool()
async def cat_fact() -> dict:
    """
    Retrieves a random cat fact from the Cat Facts API.
    """
    # We are calling the function from app.py (no await since it is synchronous)
    print("Getting cat fact")
    result = get_cat_fact()
    print("Cat fact retrieved:", result)
    return result

if __name__ == "__main__":
    print("Starting Cat MCP server")
    mcp.run(transport="streamable-http")