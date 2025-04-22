import asyncio
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Body

app = FastAPI()
  
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
    else:
        return TODO_LIST
    

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="Todo not found")
    

@app.post("/todo", response_model=Todo, name= "Create TODO",
         summary="Create a TODO element",
         description="Create a TODO element given an id, a description and completion status",
         status_code=201, deprecated=False)
async def create_todo(data: Todo):
    TODO_LIST.append(data)
    return data

@app.get("/async-endpoint")
async def async_example():
    print(f"Execution started at: {datetime.now()}", flush=True)
    await asyncio.sleep(2)
    return {"message": "Async endpoint"}