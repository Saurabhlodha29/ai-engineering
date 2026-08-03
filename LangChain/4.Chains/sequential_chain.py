from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct"
)

model = ChatHuggingFace(llm = llm)

prompt1 = PromptTemplate(
    template = "Generate a detailed report on the topic : {topic}.",
    input_variables = ["topic"]
)

parser = StrOutputParser()

prompt2 = PromptTemplate(
    template = "Generate a summary of 5 points based on the report \n {report}.",
    input_variables = ["report"]
)

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({"topic" : "Unemployment in India"})

# print(result)

chain.get_graph().print_ascii()