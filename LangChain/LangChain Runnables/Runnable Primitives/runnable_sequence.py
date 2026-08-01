from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatHuggingFace(
    llm = HuggingFaceEndpoint(
        repo_id = "Qwen/Qwen2.5-7B-Instruct"
    )
)

prompt1 = PromptTemplate(
    template = "Give me a joke about {topic}.",
    input_variables = ["topic"]
)

prompt2 = PromptTemplate(
    template = "Explain this joke to me in simple terms: {joke}.",
    input_variables = ["joke"]
)

parser = StrOutputParser()

chain = RunnableSequence(prompt1, model, parser, prompt2, model, parser)

result = chain.invoke({"topic" : "Freedom"})

print(result)