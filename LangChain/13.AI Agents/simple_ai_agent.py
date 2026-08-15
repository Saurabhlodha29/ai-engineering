# This is a simple AI agent that performs a web search for finding the relevance to the user query and hence giving the output accordingly.

from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
from dotenv import load_dotenv

load_dotenv()

# Step-1 : Create search tool and llm
search_tool = DuckDuckGoSearchRun()

llm = ChatGroq(model = "llama-3.3-70b-versatile")

# Step-2 : Pull the ReAct prompt from LangSmith hub ::::: ReAct = Reasoning + Action
client = Client()

prompt = client.pull_prompt(
    "hwchase17/react",
    include_model = False,
    dangerously_pull_public_prompt = True
)

# Prompt fetched :

# Answer the following questions as best you can. You have access to the following tools:
# {tools}
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question
# Begin!
# Question: {input}
# Thought:{agent_scratchpad}

# Step-3 : Create a ReAct Agent manually with pulled prompt
agent = create_react_agent(
    llm = llm,
    tools = [search_tool],
    prompt = prompt
)

# Step-4 : Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent = agent,
    tools = [search_tool],
    verbose = True
)

# Step-5 : Invoke
response = agent_executor.invoke({"input":"How many metro lines are there in the capital of India?"})
print(response)