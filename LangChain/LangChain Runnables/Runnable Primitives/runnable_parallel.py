from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model1 = ChatHuggingFace(
    llm = HuggingFaceEndpoint( repo_id = "Qwen/Qwen2.5-7B-Instruct" )
)

model2 = ChatGroq(
    model = "llama-3.3-70b-versatile",
)

prompt1 = PromptTemplate(
    template = "Generate a catchy/interesting tweet on the topic : {topic}",
    input_variables = ["topic"]
)

prompt2 = PromptTemplate(
    template = "Generate a catchy/interesting LinkedIn post on the topic : {topic}",
    input_variables = ["topic"]
)

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
        "tweet": RunnableSequence(prompt1, model1, parser),
        "linkedin_post": RunnableSequence(prompt2, model2, parser)
    }
)

output = parallel_chain.invoke({"topic": "AI Engineering Career Potential"})

print(output["tweet"])
print("--------------------------------------------------\n")
print(output["linkedin_post"])