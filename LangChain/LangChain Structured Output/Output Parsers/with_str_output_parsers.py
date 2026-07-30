from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct",
    task = "text-generation"
)

model = ChatHuggingFace(llm = llm)

#1st Prompt - Detailed Report
template1 = PromptTemplate(
    template = "Write a detailed report on {topic}.",
    input_variables = ["topic"]
)

#2nd Prompt - Summary
template2 = PromptTemplate(
    template = "Write the summary on the following text /n {text} \n in 5 lines.",
    input_variables = ["text"]
)

#Creating Output Parser
parser = StrOutputParser()

#Forming Chain
chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic":"Black Holes"})

print(result)