from fastapi import APIRouter, HTTPException
from api.models import TodoItem

router = APIRouter()
todos = []

@router.get("/todos")
async def get_todos():
    return todos