from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",  # default Ollama URL
    temperature=0,  # 0 = more deterministic, better for agents
)
response = llm.invoke("what do u know about the project I m working on right now ?")
print(response.content)