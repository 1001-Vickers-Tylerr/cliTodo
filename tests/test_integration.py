import pytest
import httpx
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_URL = "http://127.0.0.1:8000"

@pytest.fixture(autouse=True)
def clear_todos():
    """Clear todos before each test."""
    global todos
    from api.routes import todos
    todos.clear()

def test_add_and_verify():
    todo = {"id": 1, "task": "Test task", "priority": 1}
    response = client.post("/todos", json=todo)
    assert response.status_code == 200
    response = client.get("/todos")
    assert response.json() == [todo]

def test_update_priority():
    todo = {"id": 2, "task": "Test task", "priority": 1}
    client.post("/todos", json=todo)
    updated_todo = {"id": 2, "task": "Test task", "priority": 5}
    response = client.put("/todos/2", json=updated_todo)
    assert response.status_code == 200
    response = client.get("/todos")
    assert response.json() == [updated_todo]

def test_delete_by_id():
    todo = {"id": 3, "task": "Test task", "priority": 1}
    client.post("/todos", json=todo)
    response = client.delete("/todos/3")
    assert response.status_code == 200
    response = client.get("/todos")
    assert todo not in response.json()

def test_add_multiple_and_sort():
    todos = [
        {"id": 4, "task": "Low", "priority": 3},
        {"id": 5, "task": "High", "priority": 1}
    ]
    for todo in todos:
        client.post("/todos", json=todo)
    response = client.get("/todos")
    assert response.json() == [
        {"id": 5, "task": "High", "priority": 1},
        {"id": 4, "task": "Low", "priority": 3}
    ]

def test_delete_nonexistent():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"