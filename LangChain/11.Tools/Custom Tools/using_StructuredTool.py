from langchain_community.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(required = True, description = "The first number")
    b: int = Field(required = True, description = "The second number")

def multiplyfunc(a,b) -> int:
    return a*b

multiply_tool = StructuredTool.from_function(
    func = multiplyfunc,
    name = "multiply",
    description = "Multiply two numbers",
    args_schema = MultiplyInput
)

result = multiply_tool.invoke({"a":4,"b":5})

print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)

# print(multiply.args_schema.model_json_schema())