from langchain_core.tools import tool
from react_loop import run_agent

@tool
def get_products() -> str:
    """Returns a list of products from DefectDojo."""
    return "Product 1: WebApp, Product 2: MobileApp"

tools = [get_products]

result = run_agent("what are the main differences between each product ?", tools)
print("\n🤖 Final answer:", result)