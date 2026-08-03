#This code is actually a template for using an LLM model whihc requires API key.
#The model we currently used is Google's free chat model. LLM models are paid and require API key to use.
#So we have used a free chat model which does not require any API key.
#The code is for LLM model but what we used in the code is a chat model.

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-flash-latest")

result = llm.invoke("What is the Capital of India?")

print(result)