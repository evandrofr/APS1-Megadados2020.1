from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Hello World
@app.get("/")
def root():
    """
    Primeiros passos utilizando FastAPI. Hello World!
    """
    return {"Hello":"World"}

# Criando modelo de usuário
class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False

# Criando base de dados a partir do modelo de usuário
db = [
    Task(id = 0, title = "Louça", description = "Lava toda a louça da pia"),
    Task(id = 1, title = "Pintura", description = "Pintar a parede da sala"),
    Task(id = 2, title = "Lampada", description = "Trocar a lampada do quarto"),
    Task(id = 3, title = "Tarefa", description = "Fazer toda a tarefa de casa"),
    Task(id = 4, title = "Lavar roupa", description = "Lavar roupa das crianças")
]

# Get tasks
@app.get("/tasks")
def get_tasks():
    """
    Pegar todas as tarefas do banco de dados
    """
    return db

# Get unique task
@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """
    Pegar uma única tarefa por meio de seu id
    """
    for task in db:
        if(task.id == task_id):
            return task
    return { "Status": 404, "Message": "Task not found"}

# Post task
@app.post("/tasks")
def post_task(task_title: str, task_description: str):
    """
    Insere uma nova tarefa no banco de dados
    """
    if len(db) > 0:
        new_id = db[-1].id + 1
    else:
        new_id = 0
    new_task = Task(id = new_id, title = task_title, description = task_description)
    db.append(new_task)
    return { "Status": 201, "Messege":"Success in insert new task"}

# Update task
@app.put("/tasks/update")
def update_task(task: Task):
    """
    Atualiza as informações de uma tarefa já existente no banco de dados
    """
    for db_task in db:
        if(task.id == db_task.id):
            db[task.id] = task
            return { "Status": 200, "Message": "Success in update"}
    return { "Status": 204, "Message": "Task not found"}

# Complete task
@app.put("/tasks/complete")
def complete_task(task_id: int):
    """
    Completa uma tarefa já existente no banco de dados mudando seu status. Caso ela já esteja completa, o status voltará a ser incompleta.
    """
    for db_task in db:
        if(task_id == db_task.id):
            db[task_id].done = not db[task_id].done
            return { "Status": 200, "Message": "Success in update"}
    return { "Status": 204, "Message": "Task not found"}

# Delete task
@app.delete("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    """
    Deleta uma tarefa do banco de dados por meio do id
    """
    for task in db:
        if(task.id == task_id):
            del(db[task_id])
            return { "Status": 200, "Message": "Success in delete task"}
    return { "Status": 404, "Message": "Task not found"}