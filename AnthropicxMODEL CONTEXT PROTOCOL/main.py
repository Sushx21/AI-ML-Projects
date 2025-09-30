# D:\MCP_HRMS\main.py
from mcp.server import Server

# Create MCP server
server = Server("mcp-hrms")

# Define the function
def say_hello():
    return "Hello from HRMS MCP!"

# Register it manually as a tool
server.register_tool(
    name="say_hello",
    description="Returns a friendly hello message from HRMS",
    func=say_hello
)

if __name__ == "__main__":
    server.run()