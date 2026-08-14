from langchain_core.messages import HumanMessage
from langchain_core.tools import InjectedToolArg
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from typing import Annotated
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """ This tool fetches a conversion factor between a base currency and a target currency. """
    
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    
    response = requests.get(url)
    
    return response.json()["conversion_rate"]


@tool
def convert(base_currency_amount: int, conversion_factor: Annotated[float, InjectedToolArg]) -> float:
    """ This tool uses the conversion factor obtained to reach to the final converted currency by multiplying it with the original currency amount. """
    return base_currency_amount * conversion_factor


# Tool Binding 
llm = ChatGroq(model = "llama-3.3-70b-versatile")

llm_with_tools = llm.bind_tools([get_conversion_factor,convert])

# Tool Calling

messages = [HumanMessage("Tell me the conversion factor between Indian currency and American currency. Also convert $34 into rupees.")]

# Adding AI message to messages
ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)


for tool_call in ai_message.tool_calls:
    
    # Execute the 1st tool and get conversion factor
    if tool_call['name'] == "get_conversion_factor":
        tool_message1 = get_conversion_factor.invoke(tool_call)
        
        # Fetch the conversion factor
        conversion_factor = json.loads(tool_message1.content)
        
        # Append the obtained tool message to messages
        messages.append(tool_message1)
        
    # Execute the 2nd tool using the conversion factor from tool-1
    if tool_call["name"] == "convert":
        
        # Inject the conversion_factor into convert tool's arguments since it requires both original amount and factor
        tool_call["args"]["conversion_factor"] = conversion_factor

        tool_message2 = convert.invoke(tool_call)
        
        # Append the obtained tool message to messages
        messages.append(tool_message2)
        
print(llm_with_tools.invoke(messages).content)