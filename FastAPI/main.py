from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Hello World
@app.get("/")
def root():
    """
    Primeiros passos utilizando FastAPI. Hello World!
    """
    return {"Hello":"World"}

# Criando modelo de usuário
class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

# Criando base de dados a partir do modelo de usuário
db = [
    User(id = 1, name = "Evandro", email = "evandro@email.com", password = "evandro123"),
    User(id = 2, name = "Michel", email = "michel@email.com", password = "michel123"),
    User(id = 3, name = "Rodrigo", email = "rodrigo@email.com", password = "rodrigo123"),
    User(id = 4, name = "Abel", email = "abel@email.com", password = "abel123"),
    User(id = 5, name = "Ester", email = "ester@email.com", password = "ester123")
]

# Get users
@app.get("/users")
def get_users():
    """
    Pegar todos os usuários do banco de dados
    """
    return db

# Get unique user
@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    """
    Pegar um único usuário por meio de seu id
    """
    for user in db:
        if(user.id == user_id):
            return user
    return { "Status": 404, "Message": "User not found"}

# Post user
@app.post("/users")
def post_user(user: User):
    """
    Insere um novo usuário no banco de dados
    """
    user.id = db[-1].id + 1
    db.append(user)

# Update user
@app.put("/users/update")
def update_user(user: User):
    """
    Atualiza as informações de um usuário já existente no banco de dados
    """
    for db_user in db:
        if(user.id == db_user.id):
            db[user.id - 1] = user
            return { "Status": 200, "Message": "Success in update"}
    return { "Status": 404, "Message": "User not found"}

# Delete user
@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int):
    """
    Deleta um usuário do banco de dados por meio do id
    """
    for user in db:
        if(user.id == user_id):
            del(db[user_id - 1])
            return { "Status": 200, "Message": "Success in delete user"}
    return { "Status": 404, "Message": "User not found"}