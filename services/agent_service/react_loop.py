# agent/react_loop.py
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from config import settings
from tools import tools
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
    )


def run(user_message: str, history: list = []) -> str:
    agent = get_agent()

    messages = history + [HumanMessage(content=user_message)]

    result = agent.invoke({"messages": messages})

    # Last message in the result is the final answer
    return result["messages"][-1].content