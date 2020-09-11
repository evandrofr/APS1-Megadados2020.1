from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Hello World
@app.get("/")
def root():
    """
    Primeiros passos utilizando FastAPI.\n
    Hello World!
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
    Pegar todas as tarefas do banco de dados.\n
    Retorna uma lista de objetos json com as chaves e valores id: (int), title: (str), description: (str) e done: (bool)
    """
    return db
# Get incomplete tasks
@app.get("/tasks/notdone")
def get_incomplete_tasks():
    """
    Pegar todas as tarefas não concluidas do banco de dados.\n
    Retorna uma lista de objetos json com as chaves e valores id: (int), title: (str), description: (str) e done: (bool)
    """
    db_not_done = []
    for task in db:
        if not task.done:
            db_not_done.append(task)
    if len(db_not_done) > 0:
        return db_not_done
    return { "Status": 204, "Message": "Task not found" }

# Get complete tasks
@app.get("/tasks/done")
def get_complete_tasks():
    """
    Pegar todas as tarefas concluidas do banco de dados.\n
    Retorna uma lista de objetos json com as chaves e valores id: (int), title: (str), description: (str) e done: (bool)
    """
    db_done = []
    for task in db:
        if task.done:
            db_done.append(task)
    if len(db_done) > 0:
        return db_done
    return { "Status": 204, "Message": "Task not found" }

# Get unique task
@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """
    Pegar uma única tarefa por meio de seu id.\n
    Recebe um int que representa o id da task e retorna um objeto json com as chaves e valores id: (int), title: (str), description: (str) e done: (bool)
    """
    for task in db:
        if(task.id == task_id):
            return task
    return { "Status": 204, "Message": "Task not found" }

# Post task
@app.post("/tasks")
def post_task(task_title: str, task_description: str):
    """
    Insere uma nova tarefa no banco de dados.\n
    """
    if len(db) > 0:
        new_id = db[-1].id + 1
    else:
        new_id = 0
    new_task = Task(id = new_id, title = task_title, description = task_description)
    db.append(new_task)
    return { "Status": 201, "Messege":"Success in insert new task" }

# Update task
@app.put("/tasks/update")
def update_task(task: Task):
    """
    Atualiza as informações de uma tarefa já existente no banco de dados.\n
    Recebe um objeto json com as seguintes chaves e valores id: (int), title: (str), description: (str) e done: (bool), insere o objeto no banco de dados na última posição da lista e retorna um objeto json com as chaves e valores Status: (int) e Message: (str).
    """
    for db_task in db:
        if(task.id == db_task.id):
            db[task.id] = task
            return { "Status": 200, "Message": "Success in update" }
    return { "Status": 204, "Message": "Task not found" }

# Complete task
@app.put("/tasks/complete")
def complete_task(task_id: int):
    """
    Completa uma tarefa já existente no banco de dados mudando seu status. Caso ela já esteja completa, o status voltará a ser incompleta.\n
    Recebe um int que representa o id da task, altera o valor booleano do campo done e retorna um objeto json com as chaves e valores Status: (int) e Message: (str).
    """
    for db_task in db:
        if(task_id == db_task.id):
            db[task_id].done = not db[task_id].done
            return { "Status": 200, "Message": "Success in update" }
    return { "Status": 204, "Message": "Task not found" }

# Delete task
@app.delete("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    """
    Deleta uma tarefa do banco de dados por meio do id.\n
    Recebe um int que representa o id da task, remove o objeto json que possui esse id da lista e retorna um objeto json com as chaves e valores Status: (int) e Message: (str).
    """
    for task in db:
        if(task.id == task_id):
            del(db[task_id])
            return { "Status": 200, "Message": "Success in delete task" }
    return { "Status": 404, "Message": "Task not found" }