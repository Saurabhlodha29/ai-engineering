from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableSequence, RunnableParallel, RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

prompt = PromptTemplate(
    template = "Tell me a funny joke about the topic : {topic}",
    input_variables = ["topic"]
)

parser = StrOutputParser()

def count_words(joke: str):
    return len(joke.split())


joke_gen_chain = RunnableSequence(prompt, model, parser)

parallel_chain = RunnableParallel(
    {
        "Word_count" : RunnableLambda(count_words),
        "Joke" : RunnablePassthrough()
    }
)

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)

result = final_chain.invoke({"topic" : "Global Warming"})

print(result)