from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo, Status, TodoCreate
from uuid import uuid4, UUID

app = FastAPI()

db: List[Todo] = [
    Todo(
        id = uuid4(),
        title = "Learning FastAPI",
        completion_status = "in progress"
    ),

    Todo(
        id = uuid4(),
        title = "Understand RAG pipelines",
        completion_status = "pending"
    )
]

@app.get("/todos")
async def get_all_todos():
    if len(db) == 0:
        raise HTTPException(
            status_code = 404,
            detail = "No TODO in the database"
        )
    return db

@app.get("/todos/{title}")
async def get_todo(title: str):
    if len(db) == 0:
        raise HTTPException(
            status_code = 404,
            detail = "No TODO in the database"
        )
    for todo in db:
        if todo.title == title:
            return todo
    raise HTTPException(
        status_code = 404,
        detail = "TODO not found"
    )

@app.post("/todos")
async def create_todo(todo: TodoCreate):
    if len(todo.title) == 0:
        raise HTTPException(
            status_code = 400,
            detail = "TODO title cannot be empty"
        )

    for existing_todo in db:
        if existing_todo.title == todo.title:
            raise HTTPException(
                status_code = 400,
                detail = "TODO with this title already exists"
            )

    new_todo = Todo(
        title = todo.title,
        completion_status = todo.completion_status
    )
    db.append(new_todo)
    return db

@app.patch("/todos/{old_todo_title}/title")
async def update_todo_title(old_todo_title:str, new_todo_title:str):
    
    for todo in db:
        if todo.title == old_todo_title:
            todo.title = new_todo_title
            todo.completion_status = Status.pending
            return todo
    
    raise HTTPException(
        status_code = 404,
        detail = f"No TODO with title {old_todo_title} found!"
    )
            
@app.patch("/todos/{todo_title}/status")
async def update_todo_status(todo_title:str, new_todo_status:str):
    for todo in db:
        if todo.title == todo_title:
            if new_todo_status.lower() == "completed":
                todo.completion_status = Status.completed
                return todo
            elif new_todo_status.lower() == "in progress":
                todo.completion_status = Status.inProgress
                return todo
            elif new_todo_status.lower() == "pending":
                todo.completion_status = Status.pending
                return todo
            else:
                raise HTTPException(
                    status_code = 400,
                    detail = "Invalid status type"
                )

    raise HTTPException(
        status_code = 404,
        detail = "TODO Not Found"
    )

@app.delete("/todos")
async def delete_todo(title: str):
    for todo in db:
        if todo.title == title:
            db.remove(todo)
            return f"Todo with title {todo.title} has been deleted Successfully!"
        
    raise HTTPException(
        status_code = 404,
        detail = f"TODO with title {title} not found!"
    )