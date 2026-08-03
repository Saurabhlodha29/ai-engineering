from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv

load_dotenv()

#This 7 billion parameter is a little heavier to run at complete capacity on the current local machine
#It will require pytorch and transformers to be installed in the local environment in order to run it locally with trimmed off precision 

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    pipeline_kwargs={"temperature": 0.7, "max_new_tokens": 100}
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("Tell me a poem on potato")

print(result.content)

