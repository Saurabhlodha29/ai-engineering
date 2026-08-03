from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct",
    task = "text-generation"
)

model = ChatHuggingFace(llm = llm)

class Person(BaseModel):
    
    name : str = Field(description = "Name of the person.")
    age : int = Field(gt=18, description = "Age of the person.")
    city : str = Field(description = "Name of the city Person belongs to.")

parser = PydanticOutputParser(pydantic_object = Person)

template = PromptTemplate(
    template = "Generate the name, age and city of a fiction {place} character \n {format_instructions}",
    input_variables = ["place"],
    partial_variables = {"format_instructions" : parser.get_format_instructions()}
)

# prompt = template.invoke({"place":"Indian"})

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)

#Using Chain

chain = template | model | parser

result = chain.invoke({"place":"India"})

print(result)