import click
import httpx

API_URL = "http://127.0.0.1:8000"

@click.group()
def cli():
    pass

@cli.command()
def list():
    try:
        response = httpx.get(f"{API_URL}/todos")
        response.raise_for_status()
        for todo in response.json():
            click.echo(f"ID: {todo['id']}, Task: {todo['task']}, Priority: {todo['priority']}")
    except httpx.HTTPError as e:
        click.echo(f"Error fetching todos: {e}")

@cli.command()
@click.argument("task")
@click.option("--priority", default=1, type=int, help="Priority of the task")
def add(task, priority):
    try:
        response = httpx.get(f"{API_URL}/todos")
        response.raise_for_status()
        new_id = len(response.json()) + 1
        todo = {"id": new_id, "task": task, "priority": priority}
        response = httpx.post(f"{API_URL}/todos", json=todo)
        response.raise_for_status()
        click.echo(f"Added task: ID={new_id}, Task={task}, Priority={priority}")
    except httpx.HTTPError as e:
        click.echo(f"Error adding todo: {e}")

@cli.command()
@click.argument("id", type=int)
@click.option("--task", help="New task description")
@click.option("--priority", type=int, help="New priority")
def update(id, task, priority):
    try:
        response = httpx.get(f"{API_URL}/todos")
        response.raise_for_status()
        current_todo = next((todo for todo in response.json() if todo["id"] == id), None)
        if not current_todo:
            click.echo(f"Error: Todo with ID {id} not found")
            return
        todo = {
            "id": id,
            "task": task if task else current_todo["task"],
            "priority": priority if priority else current_todo["priority"]
        }
        response = httpx.put(f"{API_URL}/todos/{id}", json=todo)
        response.raise_for_status()
        click.echo(f"Updated task: ID={id}, Task={todo['task']}, Priority={todo['priority']}")
    except httpx.HTTPError as e:
        click.echo(f"Error updating todo: {e}")

@cli.command()
@click.argument("id", type=int)
def delete(id):
    try:
        response = httpx.delete(f"{API_URL}/todos/{id}")
        response.raise_for_status()
        click.echo(f"Deleted task: ID={id}")
    except httpx.HTTPError as e:
        click.echo(f"Error deleting todo: {e}")

if __name__ == "__main__":
    cli()