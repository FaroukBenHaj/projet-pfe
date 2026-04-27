# Fix — register tools before running
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from tools import ( 
    products_type_tools ,
    products_tools,
    engagements_tools,
    test_tools,
    test_types_tools,
    findings_tools
    ) #, findings_tools, engagements_tools
load_dotenv()

app = FastMCP("defectdojo", stateless_http=True, port=8081)
findings_tools.register_tools(app)
products_type_tools.register_tools(app)
products_tools.register_tools(app)
engagements_tools.register_tools(app)
test_tools.register_tools(app)
test_types_tools.register_tools(app)
if __name__ == "__main__":
    app.run(transport="streamable-http")

