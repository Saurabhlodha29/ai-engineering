#So the purpose is to convert all the components into runnables that are standardized, and alloting them common methods with same names (The main one out of them is .invoke() method).

#We will use the concept of abstraction for that.

#For that, will create an abstract class called Runnable, which will have the common methods that all the components will have, and then we will create the standardized components by inheriting the Runnable class.

from abc import ABC, abstractmethod

class Runnable(ABC):
    
    #The main invoke() method will not do anything in this parent class, but it will implement different functionalities in the child classes, and all the child classes will have the same method name. This forces all the Child classes to use invoke() method and assign it a functionality.
    @abstractmethod
    def invoke(input_dict):
        pass


import random
class DummyLLM(Runnable):
    
    def __init__(self):
        return None
    
    #Here invoke will do the same fucntionality as predict before.
    def invoke(self, prompt):
        response_list = [
            "Delhi is the Capital of India.",
            "IPL is a cricket league in India.",
            "AI stands for Artifical Intelligence.",
        ]
                
        return {"response": random.choice(response_list)}
        
    
class DummyPromptTemplate(Runnable):
    
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables
        
    #Here invoke will do the same fucntionality as format before.
    def invoke(self, input_dict):
            return {"joke": self.template.format(**input_dict)}
        
#We will create a Parser component to get the string out of the dictionar output

class DummyStrOutputParser(Runnable):
    
    def __init__(self):
        pass
    
    def invoke(self, input_dict):
        return input_dict["response"]
        
#Now we can create a chain of any length out of these standardized components, and for that we will create another class RunnableConnector.

class RunnableConnector(Runnable):
    
    def __init__(self, runnable_list):
        self.runnable_list = runnable_list
        
    def invoke(self, input_data):
        
        for runnable in self.runnable_list:
            input_data = runnable.invoke(input_data)
            
        return input_data
    
llm = DummyLLM()

prompt1 = DummyPromptTemplate(
    template = "Write a joke on {topic}.",
    input_variables = ["topic"]
)

prompt2 = DummyPromptTemplate(
    template = "Explain the joke {response} in simple way.",
    input_variables = ["response"]
)

parser = DummyStrOutputParser()

chain1 = RunnableConnector([prompt1, llm])

chain2 = RunnableConnector([prompt2, llm, parser])

final_chain = RunnableConnector([chain1, chain2])
final_result = final_chain.invoke({"topic" : "Freedom"})

print(final_result)