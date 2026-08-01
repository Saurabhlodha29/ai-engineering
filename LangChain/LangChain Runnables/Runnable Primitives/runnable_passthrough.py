from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableSequence, RunnableParallel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

prompt1 = PromptTemplate(
    template = "Tell me a funny joke about the topic : {topic}",
    input_variables = ["topic"]
)

prompt2 = PromptTemplate(
    template = "Explain the joke in simple terms, joke : {joke}",  
    input_variables = ["joke"]
)

parser = StrOutputParser()

joke_generator_chain = RunnableSequence(prompt1, model, parser)


parallel_chain = RunnableParallel({
    "joke" : RunnablePassthrough(),
    "explanation" : RunnableSequence(joke_generator_chain,prompt2,model,parser)
})

final_chain = RunnableSequence(joke_generator_chain, parallel_chain)
output = final_chain.invoke({"topic": "Freedom Fighters"})
print(output)