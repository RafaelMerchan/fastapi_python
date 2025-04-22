from typing import Annotated
from fastapi import Form, APIRouter

router = APIRouter(
    prefix="/support",
    tags=["Support"]
)

@router.post("")
async def create_support_ticket(title: Annotated[str, Form()], message: Annotated[str, Form()]):
    return {"title": title, "message": message}
