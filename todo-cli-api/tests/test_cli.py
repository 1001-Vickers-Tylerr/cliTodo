from click.testing import CliRunner
from cli.todo import cli
import pytest
import httpx

API_URL = "http://127.0.0.1:8000"

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_httpx(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self._json = json_data
            self.status_code = status_code

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"Client error '{self.status_code}'",
                    request=None,
                    response=self
                )

    class MockClient:
        def __init__(self):
            self.responses = {}

        def add_response(self, method, url, json_data, status_code=200):
            self.responses[(method, url)] = MockResponse(json_data, status_code)

        def get(self, url, *args, **kwargs):
            return self.responses.get(('GET', url), MockResponse({}, 404))

        def post(self, url, *args, **kwargs):
            return self.responses.get(('POST', url), MockResponse({}, 404))

        def put(self, url, *args, **kwargs):
            return self.responses.get(('PUT', url), MockResponse({}, 404))

        def delete(self, url, *args, **kwargs):
            return self.responses.get(('DELETE', url), MockResponse({}, 404))

    mock_client = MockClient()
    monkeypatch.setattr(httpx, "get", mock_client.get)
    monkeypatch.setattr(httpx, "post", mock_client.post)
    monkeypatch.setattr(httpx, "put", mock_client.put)
    monkeypatch.setattr(httpx, "delete", mock_client.delete)
    return mock_client

def test_list_empty(runner, mock_httpx):
    mock_httpx.add_response('GET', f"{API_URL}/todos", [], 200)
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No todos found" in result.output

def test_list_todos(runner, mock_httpx):
    mock_httpx.add_response('GET', f"{API_URL}/todos", [
        {"id": 1, "task": "Test task", "priority": 1}
    ], 200)
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "ID: 1, Task: Test task, Priority: 1" in result.output

def test_add_todo(runner, mock_httpx):
    mock_httpx.add_response('GET', f"{API_URL}/todos", [], 200)
    mock_httpx.add_response('POST', f"{API_URL}/todos", {"id": 1, "task": "Test task", "priority": 1}, 200)
    result = runner.invoke(cli, ["add", "Test task", "--priority", "1"])
    assert result.exit_code == 0
    assert "Added task: ID=1, Task=Test task, Priority=1" in result.output

def test_update_todo(runner, mock_httpx):
    mock_httpx.add_response('GET', f"{API_URL}/todos", [
        {"id": 2, "task": "Test task", "priority": 1}
    ], 200)
    mock_httpx.add_response('PUT', f"{API_URL}/todos/2", {"id": 2, "task": "Test task", "priority": 5}, 200)
    result = runner.invoke(cli, ["update", "2", "--priority", "5"])
    assert result.exit_code == 0
    assert "Updated task: ID=2, Task=Test task, Priority=5" in result.output

def test_delete_todo(runner, mock_httpx):
    mock_httpx.add_response('DELETE', f"{API_URL}/todos/3", {"detail": "Todo with ID 3 deleted"}, 200)
    result = runner.invoke(cli, ["delete", "3"])
    assert result.exit_code == 0
    assert "Deleted task: ID=3" in result.output