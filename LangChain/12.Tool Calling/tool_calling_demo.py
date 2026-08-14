from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests

load_dotenv()

# 1.Creation

@tool
def multiply(a:int, b:int) -> int:
    """Given two numbers a and b this tool returns their product"""
    return a * b

# 2.Binding

llm = ChatHuggingFace(llm = HuggingFaceEndpoint(repo_id = "Qwen/Qwen2.5-7B-Instruct"))

llm_with_tools = llm.bind_tools([multiply])

# 3.Calling

query = HumanMessage("Can you multiply 2 with 4")   # Human message is added

messages = [query]

call = llm_with_tools.invoke(messages)     # Initial execution

messages.append(call)      # AI message is added

# 4.Execution

tool_result = multiply.invoke(call.tool_calls[0])

messages.append(tool_result)    # Tool message is added

final_result = llm_with_tools.invoke(messages)    # Final execution

print(final_result.content)