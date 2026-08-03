from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name : str 
    age : Optional[int] = None
    email : EmailStr
    cgpa : float = Field(gt = 0, lt = 10, default = 5, description = "This float number represents the cgpa of a student")

#This will raise an error if we try to Enter another data type instead of str in "name"
new_student = {"name" : "Saurabh", "age" : 20, "email" : "abc@gmail.com", "cgpa" : 9.32}

student = Student(**new_student)

student_dict = dict(student)
print(student_dict["age"]) 