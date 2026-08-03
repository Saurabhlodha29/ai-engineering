from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4")

# .invoke() sends a message, gets a structured AIMessage back
result = model.invoke("What is the capital of India?")

print(result.content)
# Output: "New Delhi is the capital of India"