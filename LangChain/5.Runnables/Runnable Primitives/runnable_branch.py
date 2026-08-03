from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableSequence, RunnableParallel, RunnableLambda, RunnableBranch
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template = "Write a detailed report about the topic : {topic}.",
    input_variables = ["topic"]
)

prompt2 = PromptTemplate(
    template = "Summarize the report: \n {report} \n in less than 500 words.",
    input_variables = ["report"]
)


report_gen_chain = RunnableSequence(prompt1, model, parser)

conditional_chain = RunnableBranch(
    (lambda x: len(x.split()) >= 500, RunnableSequence(prompt2, model, parser)),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_gen_chain, conditional_chain)

result = final_chain.invoke({"topic" : "Global Warming"})

print(result)