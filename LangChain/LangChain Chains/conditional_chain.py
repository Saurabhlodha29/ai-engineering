from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct"
)

model = ChatHuggingFace(llm = llm)

parser1 = StrOutputParser()

class Feedback(BaseModel):
    sentiment : Literal["Positive","Negative"] 

parser2 = PydanticOutputParser(pydantic_object = Feedback)

prompt1 = PromptTemplate(
    template = "Classify the Sentiment of the following feedback as Positive or Negative : \n {feedback} \n {format_instruction}.",
    input_variables = ["feedback"],
    partial_variables = {"format_instruction" : parser2.get_format_instructions()}
)

prompt2 = PromptTemplate(
    template = "Return an appropriate reply to this positive Review : {feedback}.", 
    input_variables = ["feedback"]
)

prompt3 = PromptTemplate(
    template = "Write and appropriate reply to this negative Review : {feedback}.", 
    input_variables = ["feedback"]
)

classifier_chain = prompt1 | model | parser2

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == "Positive", prompt2 | model | parser1),
    (lambda x:x.sentiment == "Negative", prompt3 | model | parser1),
    RunnableLambda(lambda x: "Could not find sentiment.")
) 

final_chain = classifier_chain | branch_chain

result = final_chain.invoke({"feedback" : "This phone is terrible."})

# print(result)

final_chain.get_graph().print_ascii()