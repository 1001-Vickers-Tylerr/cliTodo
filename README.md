# To-Do List CLI and API

A simple To-Do List application with a CLI and REST API.

## Deploy to Heroku

Deploy this app to your Heroku account with one click:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/1001-Vickers-Tylerr/cliTodo)

Once downloaded, note your URL.

Clone the repo: 

```
git clone https://github.com/1001-Vickers-Tylerr/cliTodo.git
cd cliTodo
pip install pyinstaller
sed -i 's|API_URL = "http://127.0.0.1:8000"|API_URL = "https://your-app-name.herokuapp.com"|' cli/todo.py
pyinstaller --onefile cli/todo.py
```

Then, use the binary in dist/todo

## Download and use CLI

Visit the GitHub release at
https://github.com/1001-Vickers-Tylerr/cliTodo/releases/tag/v1.0.0

Click todo, under Assets

Make it executable

```
chmod +x todo
```

## Commands
./todo list - lists all items
./todo add "new task" --priority <#> - adds a new task with a priority
./todo update 1 --task "updated task" --priority <#> - Updates a todo by ID
./todo delete <#> - deletes a todo by ID