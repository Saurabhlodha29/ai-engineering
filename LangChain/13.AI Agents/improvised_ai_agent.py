from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import Client
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Step-1 : Creating tools

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) ->str:
    """This function fetches the current weather data for a given city."""
    
    api_key = os.getenv("WEATHER_STACK_API_KEY")
    
    url = f"https://api.weatherstack.com/current?access_key={api_key}&query={city}"
    
    response = requests.get(url)
    
    return response.json()
   
# Step-2 : Creating Agent and Agent Executor

llm = ChatGroq(model = "llama-3.3-70b-versatile")
   
client = Client() 

prompt = client.pull_prompt(
    "hwchase17/react",
    include_model = False,
    dangerously_pull_public_prompt = True
)

agent = create_react_agent(
    prompt = prompt,
    tools = [search_tool,get_weather_data],
    llm = llm
)

agent_executor = AgentExecutor(
    agent = agent,
    tools = [search_tool,get_weather_data],
    verbose = True
)

# Step-3 : Invoke

result = agent_executor.invoke({"input":"What is the capital of Maharashtra. And also tell me the current temperature in that capital city."})
print(result)