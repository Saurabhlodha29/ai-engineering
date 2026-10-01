import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langchain_core.tools import tool
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

load_dotenv()

llm = ChatGroq(model = 'openai/gpt-oss-safeguard-20b')
   
# ------------ Tools -------------- 
@tool
def get_stock_price(symbol : str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g, 'AAPL','TSLA')
    Using Alpha Vantage with api key in the url.
    """
    
    api_key = os.environ['STOCK_API_KEY']
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    
    r = requests.get(url)
    return r.json()

@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
    Simulate purchasing a given quantity of a stock symbol.
    
    HUMAN IN THE LOOP:
    Before confirming the purchase, this tool will interrupt
    and wait for a human decision ("yes / anything else).
    """
    # This pauses the graph and handle control to the human
    decision = interrupt(f"Approve buying {quantity} shares of {symbol}? (yes/no)")
    
    if isinstance(decision, str) and decision.lower() == 'yes':
        return {
            'status':'success',
            'message':f'Purchase order placed for {quantity} shares of {symbol}',
            'symbol':symbol,
            'quantity':quantity
        }
        
    else:
        return {
            'status':'cancelled',
            'message':f'Purchase order placed for {quantity} shares of {symbol} declined by human',
            'symbol':symbol,
            'quantity':quantity
        }
        
tools = [get_stock_price, purchase_stock]

llm_with_tools = llm.bind_tools(tools)

# ------------ State -------------- 

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]
    
# ------------ Nodes -------------- 
    
def chat_node(state: ChatState):
    """LLM node that answer or request a tool call."""
    
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    
    return {'messages':[response]}

tool_node = ToolNode(tools)

# ------------ Checkpointer -------------- 

memory = MemorySaver()

# ------------ Graph -------------- 

graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools','chat_node')

chatbot = graph.compile(checkpointer = memory)

# ------------ Simple Usage Example (CLI with HITL) -------------- 

if __name__ == 'main':
    
    thread_id = 'demo-thread'
    
    while True:
        user_input = input('You: ')
        if user_input.lower().strip() in {'exit','quit'}:
            print("Goodbye!")
            break
        
        # Build initial state for this turn
        state = {'messages':[HumanMessage(content = user_input)]}
        
        # Run the graph (may hit an interrupt)
        result = chatbot.invoke(
            state,
            config = {'configurable':{'thread_id':thread_id}}
        )
        
        # Check HITL interrupt from purchase_stock
        interrupts = result.get('__interrupt__',[])
        
        if interrupts:
            # Our interrupt payload is the string we passed to interrupt(...)
            prompt_to_human = interrupts[0].value
            print(f"HITL: {prompt_to_human}")
            decision = input("You decision: ").strip().lower()
            
            # Resume graph with human decision (yes/no/whatever)
            result = chatbot.invoke(
                Command(resume = decision),
                config = {'configurable':{'thread_id':thread_id}},
            )
            
            # Get the latest message from the assistant
            messages = result['messages']
            last_msg = messages[-1]
            print(f"Bot: {last_msg.content}\n")