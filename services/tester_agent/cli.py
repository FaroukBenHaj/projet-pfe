# cli.py
from react_loop import run
from gateway.mcp_client import MCPClient
from gateway.tool_gateway import ToolGateway
from config import settings  # assuming you have MCP URL here

mcp_client = MCPClient(base_url=settings.mcp_service_base_url)
tool_gateway = ToolGateway(mcp_client)
def main():
    print("DefectDojo Tester Agent")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = run(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()