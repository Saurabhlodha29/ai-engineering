from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct"
)

model = ChatHuggingFace(llm = llm)

prompt = PromptTemplate(
    template = "Generate 5 interesting facts about {topic}",
    input_variables = ["topic"]
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic":"Cricket"})

# print(result)

chain.get_graph().print_ascii()