from langchain_google_genai import ChatGoogleGenerativeAI   
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

response = model.invoke("Tell me something about cow",temperature = 1.9)

print(response.content[0]["text"])
