from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
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
    template = "Write the summary on the following text \n {text} /n in 5 lines.",
    input_variables = ["text"]
)

prompt1 = template1.invoke({"topic":"Black Holes"})
result1 = model.invoke(prompt1)

prompt2 = template2.invoke({"text":result1})
result2 = model.invoke(prompt2)

print(result2.content)