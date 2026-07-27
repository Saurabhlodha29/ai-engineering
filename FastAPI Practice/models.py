from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from enum import Enum

class Status(str, Enum):
    completed = "completed"
    inProgress = "in progress"
    pending = "pending"

class TodoCreate(BaseModel):
    title: str
    completion_status: Status = Status.pending

class Todo(BaseModel):
    id: UUID = Field(default_factory = uuid4)
    title: str
    completion_status: Status = Status.pending