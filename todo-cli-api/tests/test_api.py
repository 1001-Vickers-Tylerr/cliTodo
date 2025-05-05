from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_add_todo():
    todo = {"id": 1, "task": "Test task", "priority": 1}
    response = client.post("/todos", json=todo)
    assert response.status_code == 200
    assert response.json() == todo
    response = client.get("/todos")
    assert response.json() == [todo]

def test_add_todo_duplicate_id():
    todo = {"id": 1, "task": "Duplicate", "priority": 2}
    response = client.post("/todos", json=todo)
    assert response.status_code == 400
    assert response.json()["detail"] == "Todo with this ID already exists."  # Added period

def test_update_todo():
    todo = {"id": 2, "task": "Test task", "priority": 1}
    client.post("/todos", json=todo)
    updated_todo = {"id": 2, "task": "Updated task", "priority": 5}
    response = client.put("/todos/2", json=updated_todo)
    assert response.status_code == 200
    assert response.json() == updated_todo
    response = client.get("/todos")
    assert updated_todo in response.json()

def test_update_todo_not_found():
    todo = {"id": 999, "task": "Missing", "priority": 1}
    response = client.put("/todos/999", json=todo)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_delete_todo():
    todo = {"id": 3, "task": "Test task", "priority": 1}
    client.post("/todos", json=todo)
    response = client.delete("/todos/3")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo with ID 3 deleted"
    response = client.get("/todos")
    assert todo not in response.json()

def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"