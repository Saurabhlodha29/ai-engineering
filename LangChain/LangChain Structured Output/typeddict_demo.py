from typing import TypedDict

class Person(TypedDict):
    name : str
    age : int
    
new_person : Person = {
    "name" : "Saurabh",
    "age" : 20
}

new_person2 : Person = {
    "name" : "Saurabh",
    "age" : '20'
}
print(new_person)
print(new_person2)