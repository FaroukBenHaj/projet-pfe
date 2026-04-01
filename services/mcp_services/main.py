# Fix — register tools before running
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from tools import (findings_tools, products_tools, engagements_tools , products_type_tools)
load_dotenv()

a = FastMCP("defectdojo", stateless_http=True, port=8081)
findings_tools.register_tools(a)
products_tools.register_tools(a)
products_type_tools.register_tools(a)
engagements_tools.register_tools(a)

if __name__ == "__main__":
    a.run(transport="streamable-http")

