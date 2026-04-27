# agent/react_loop.py
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from config import settings
from tools import AGENT_TOOLS as tools
from prompt import SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver

saver = InMemorySaver()

def get_agent():
    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )
    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=saver,
    )


def run(user_message: str , thread_id:str = "default") -> str:
    agent = get_agent()

    messages = [HumanMessage(content=user_message)]

    result = agent.invoke(
        {"messages": messages},
        {"configurable": {"thread_id": thread_id}}
        )

    # Last message in the result is the final answer
    return result["messages"][-1].content