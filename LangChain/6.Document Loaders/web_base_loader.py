from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq( model = "llama-3.3-70b-versatile")

parser = StrOutputParser()

url = "https://www.amazon.in/gp/product/B0FPRCDS5J/ref=ewc_pr_img_3?smid=A1WYWER0W24N8S&th=1"

loader = WebBaseLoader(url)

docs = loader.load()

prompt = PromptTemplate(
    template = "Extract the price and model of the given product page data : \n {page_data}",
    input_variables = ["page_data"]
)

chain = prompt | model | parser

print(chain.invoke({"page_data" : docs[0].page_content}))



# print(docs[0].page_content)
# print(len(docs))
# print(docs[0].metadata)