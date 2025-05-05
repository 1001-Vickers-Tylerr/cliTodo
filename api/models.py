from pydantic import BaseModel

class TodoItem(BaseModel):
    id: int
    task: str
    priority: int