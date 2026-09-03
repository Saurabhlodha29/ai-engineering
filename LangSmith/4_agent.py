import os
import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# CHANGED:
# We are using create_agent instead of create_react_agent.
#
# create_react_agent belongs to the older/classic ReAct approach,
# where the model generates textual "Thought / Action / Action Input"
# instructions.
#
# gpt-oss-20b supports native tool calling, so we use LangChain's
# newer create_agent API, which handles tool calling directly.
from langchain.agents import create_agent

from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_PROJECT'] = 'AI Agent'

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> str:
    """
    This function fetches the current weather data for a given city
    """
    api_key = os.getenv("WEATHER_STACK_API_KEY")

    url = f"https://api.weatherstack.com/current?access_key={api_key}&query={city}"

    response = requests.get(url)

    return response.json()


llm = ChatGroq(model="openai/gpt-oss-20b")


# Step 2: Pull the ReAct prompt from LangChain Hub
#
# CHANGED:
# We are NOT pulling the "hwchase17/react" prompt anymore.
#
# That prompt was specifically designed for the classic ReAct agent.
# The newer create_agent API does not require that ReAct prompt.
#
# Instead, create_agent can work directly with the model and tools.
# Therefore, the LangSmith Client and Hub prompt are no longer needed.


# Step 3: Create the agent
#
# CHANGED:
# Previously we used:
#
# agent = create_react_agent(
#     llm=llm,
#     tools=[search_tool, get_weather_data],
#     prompt=prompt
# )
#
# create_react_agent is the source of the tool-calling incompatibility
# we encountered with gpt-oss-20b.
#
# create_agent uses the model's native tool-calling capabilities.

agent = create_agent(
    model=llm,
    tools=[search_tool, get_weather_data],
    system_prompt="You are a helpful AI assistant. Use the available tools when necessary to answer the user's question."
)


# Step 4: Agent execution
#
# CHANGED:
# We no longer need AgentExecutor.
#
# The newer create_agent returns a LangGraph-based agent that can be
# invoked directly.
#
# Previously:
#
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[search_tool, get_weather_data],
#     verbose=True,
#     max_iterations=5
# )


# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.


# Step 5: Invoke
#
# CHANGED:
# create_agent expects the input in the "messages" format rather than
# the old AgentExecutor format {"input": "..."}.
#
# The agent returns a state containing the conversation messages.
response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Where did the Gamescom 2026 event take place, find the current temperature of that place too."
        }
    ]
})

print(response)

print(response["messages"][-1].content)