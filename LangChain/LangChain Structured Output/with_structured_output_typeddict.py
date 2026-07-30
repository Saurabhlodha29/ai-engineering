from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict,Annotated,Optional,Literal
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct"
)

model = ChatHuggingFace(llm = llm)

class Review(TypedDict):
    
    key_themes : Annotated[list[str], "Identify key themes discussed and write them down in list."]
    summary : Annotated[str, "Generate a brief summary of the review."]
    sentiment : Annotated[Literal["pos", "neg"], "Determine the sentiment of the review."]
    pros : Annotated[Optional[list[str]], "List down all the pros of the product in a list."]
    cons : Annotated[Optional[list[str]], "List down all the cons of the product in a list."]
    name : Annotated[Optional[str], "Identify the name of the reviewer. Don't make up a name if it is not mentioned in the review. If the name is not mentioned, return None."]
    
    
structured_model = model.with_structured_output(Review)

result = structured_model. invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3
processor makes everything lightning fast-whether I'm gaming, multitasking, or editing photos. The 5000mAh battery easily
lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me
away is the 200MP camera-the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x
actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with
bloatware-why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard
pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful

Cons:
Bulky and heavy-not great for one-handed use
Bloatware still exists in One UI
Expensive compared to competitors

-Review by Saurabh""")

print(result)