# #NOTE :- This code is not going to work because the latest versions of LangChain removed many APIs
# #Those removed APIs include StructuredOutputParser and ResponseSchema, they might work in the older versions (Langchain 0.3.x)
# #So they are currently not used in practiced anymore

# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from langchain_core.prompts import PromptTemplate
# from langchain.output_parsers import StructuredOutputParser,ResponseSchema
# from dotenv import load_dotenv

# load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id = "Qwen/Qwen2.5-7B-Instruct",
#     task = "text-generation"
# )

# model = ChatHuggingFace(llm = llm)

# schema = [
#     ResponseSchema(name='fact_1', description='Fact 1 about the topic'),
#     ResponseSchema(name='fact_2', description='Fact 2 about the topic'),
#     ResponseSchema(name='fact_3', description='Fact 3 about the topic')
# ]

# parser = StructuredOutputParser.from_response_schemas(schema)

# template = PromptTemplate(
#     template='Give 3 fact about {topic} \n {format_instruction} ',
#     input_variables=['topic'],
#     partial_variables={'format_instruction' :parser.get_format_instructions()}
# )

# parser = StructuredOutputParser.from_responseSchemas()

# prompt = template. invoke({'topic':'black hole'})

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)

# print(final_result)