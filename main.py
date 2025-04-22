import asyncio

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union, Optional, Annotated
from fastapi import FastAPI, HTTPException, Form, Path, File, UploadFile

app = FastAPI(
    title="TODO API",
)
  
TODO_LIST = [
    {"id": 1, "description": "Learn Python", "complete": True},
    {"id": 2, "description": "Learn FastAPI", "complete": False},
    {"id": 3, "description": "Tarea 3", "complete": False}
]


class Todo(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=5, max_length=500)
    complete: bool = Field(default=False)


@app.get("/todo")
async def get_all(complete: Union[bool, None] = None):
    if complete is not None:
        filtered_todos = list(filter(lambda todo: todo["complete"] == complete, TODO_LIST))
        return filtered_todos
    return TODO_LIST
    

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="Todo not found")
    

@app.post("/todo", 
          response_model=Todo, 
          name= "Create TODO",
         summary="Create a TODO element",
         description="Create a TODO element given an id, a description and completion status",
         status_code=201, 
         deprecated=False)
async def create_todo(data: Todo):
    TODO_LIST.append(data)
    return data


@app.get("/async-endpoint")
async def async_example():
    print(f"Execution started at: {datetime.now()}", flush=True)
    await asyncio.sleep(2)
    return {"message": "Async endpoint"}


@app.post("/support")
async def create_support_ticket(title: Annotated[str, Form()], message: Annotated[str, Form()]):
    return {"title": title, "message": message}


@app.post("/todo/{todo_id}/attachment")
async def upload_todo_file(todo_id: Annotated[int, Path()], file: UploadFile):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        todo_data["file_name"] = file.file
        file_content = await file.read()
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="Todo not found")
    




