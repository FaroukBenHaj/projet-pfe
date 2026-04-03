from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from prompt import SYSTEM_PROMPT
from llm import llm
MAX_STEPS = 10

def run_agent(user_input: str, tools: list):
    # bind tools to the LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # initialize conversation history
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]
    
    for step in range(MAX_STEPS):
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        # check if LLM wants to use a tool
        if response.tool_calls:
            for tool_call in response.tool_calls:
                # 1. find the tool by name
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id   = tool_call["id"]

                print(f"\n🔧 Agent wants to use: {tool_name}")
                print(f"   with args: {tool_args}")

                # 2. find and run the matching tool
                matching_tool = next((t for t in tools if t.name == tool_name), None)

                if matching_tool is None:
                    result = f"Error: tool '{tool_name}' not found."
                else:
                    result = matching_tool.invoke(tool_args)

                # 3. add tool result to history
                messages.append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_id,
                ))
        else:
            # LLM is done, return final answer
            return response.content
    
    return "Max steps reached. Task incomplete."