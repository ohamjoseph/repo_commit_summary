from langchain_ollama import ChatOllama

llm = ChatOllama(
    BASE_URL="localhost:11434",
    model="llama3.2",
    temperature=0.5
)