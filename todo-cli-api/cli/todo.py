import click
import httpx

API_URL = "http://localhost:8000"

@click.group()
def cli():
    pass

@cli.command()
def list():
    response = httpx.get(f"{API_URL}/todos")
    for todo in response.json():
        click.echo(f"ID: {todo['id']}, Task: {todo['task']}, Priority: {todo['priority']}")