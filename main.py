from fastapi import FastAPI
from enum import Enum
from routers import todo, support


class Tags(Enum):
    home: str = "Home"

tags_info = [{
    "name": "Home",
    "description": "Test description"
}]

app = FastAPI(
    title="TODO API",
    openapi_tags=tags_info
)

app.include_router(todo.router)
app.include_router(support.router)

@app.get("/", tags=[Tags.home])
async def home():
    return {
        "name": "TODO Rest API",
        "version": "1.0.0",
    }
