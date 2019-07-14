from fastapi import FastAPI

app = FastAPI()

class User:
    def __init__(self, username, gender, age):
        self.username = username
        self.gender = gender
        self.age = age

fakeDb = {}

fakeDb[0] = User("Joe", "M", 78)
fakeDb[1] = User("Kamala", "F", 55)
fakeDb[2] = User("Bernard", "M", 76)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    return fakeDb

@app.get("/users/{id}")
async def get_user(id: int):
    "Gets an user by id"
    user = fakeDb[id] 
    return user

@app.delete("/users/{id}")
async def delete_user(id: int):
    del fakeDb[id]

@app.get("/create-user")
async def create_user_query_string(username: str, gender: str, age: int):
    user = User(username, gender, age)
    nextId = len(fakeDb)
    fakeDb[nextId] = user

@app.get("/update-user")
async def update_user_query_string(id: int, prop: str, value: str):
    user = fakeDb[id]
    setattr(user, prop, value)