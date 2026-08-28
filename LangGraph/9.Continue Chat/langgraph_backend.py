from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

model = ChatNVIDIA(model = "openai/gpt-oss-20b")

# Define State
class MessageState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]
    
    
# Define Chatbot function
def chat_node(state : MessageState):
    messages = state['messages']
    
    response = model.invoke(messages).content
    
    return {'messages':[response]}

    
# Define Graph
graph = StateGraph(MessageState)

# Nodes & Edges
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# Checkpointer
checkpointer = InMemorySaver()

chatbot = graph.compile(checkpointer = checkpointer)
