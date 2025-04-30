from fastapi import APIRouter, HTTPException
from api.models import TodoItem

router = APIRouter()
todos = []

@router.get("/todos")
async def get_todos():
    return todos

@router.post("/todos")
async def add_todo(item: TodoItem):
    if any(todo.id == item.id for todo in todos):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists.")
    todos.append(item)
    return item