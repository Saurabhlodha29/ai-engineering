#We are trying to make the copies of predefined LangChain classes for demonstration, these classes don't inherit the original functionality, instead we will try to give them. The purpose of them is to understand the need for creating Runnables in LangChain, how the LangChain developers thought before creating the common methods for all the different components, since before that, they all used to have different names, and injection was kind of difficult back then.

import random
class DummyLLM:
    
    def __init__(self):
        return None
        
    #Since the LLM component before being discarded used to have .predict() method for generating the output, we will try to implement that here as well.
    def predict(self, prompt):
        
        response_list = [
            "Delhi is the Capital of India.",
            "IPL is a cricket league in India.",
            "AI stands for Artifical Intelligence.",
        ]
        
        return {"response": random.choice(response_list)}
    
class DummyPromptTemplate:
    
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables
        
    #Since the PromptTemplate component used to have .format() method for formatting the prompt, we will try to implement that here as well.
    def format(self, input_dict):
        return self.template.format(**input_dict)   #This is the native python formatting function which fills in the placeholders.


#Now we will create a Small LLM application using Dummy classes. The application will take a prompt template and generate a response using the DummyLLM class.

# #DummyLLM object
# llm = DummyLLM()

# #DummyPromptTemplate object
# template = DummyPromptTemplate(
#     template = "Write a {length} poem about {topic}.",
#     input_variables = ["length", "topic"]
# )
# prompt = template.format({"length": "short", "topic": "the ocean"})

# #This is the response generated (If it was a real LLM output would have been a poem about the ocean)
# output = llm.predict(prompt)
# print(output)


#So now we will create a DummyChain class to chain things together.

class DummyChain:
    
    def __init__(self, prompt, llm):
        self.prompt = prompt
        self.llm = llm
        
    #Since initially the chain component used to have .run() method for running the chain, we will try to implement that here as well.
    def run(self, input_dict):
        formatted_prompt = self.prompt.format(input_dict)
        result = self.llm.predict(formatted_prompt)
        
        return result["response"]
    
#DummyLLM object
llm = DummyLLM()

#DummyPromptTemplate object
template = DummyPromptTemplate(
    template = "Write a {length} poem about {topic}.",
    input_variables = ["length", "topic"]
)

#DummyChain object
chain = DummyChain(template, llm)
output = chain.run({"length": "short", "topic": "the ocean"})
print(output)
