from fastapi import FastAPI
from pydantic import BaseModel

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
    print("hi")
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    return fakeDb

@app.get("/users/{id}")
async def get_user(id: int):
    "Gets a user by id"
    item = fakeDb[id] 
    return item

@app.delete("/users/{id}")
async def delete_user(id: int):
    del fakeDb[id]

class UserIn(BaseModel):
    name: str
    sex: str
    age: int

@app.post("/users/")
async def create_user(userIn: UserIn):
    user = User(userIn.name, userIn.sex, userIn.age)
    fakeDb[len(fakeDb)] = user
    return user

class UpdateUserIn(BaseModel):
    username:str = None
    gender:str = None
    age:int = None

@app.patch("/users/{id}")
async def create_user(updateUserIn: UpdateUserIn, id:int):
    user = fakeDb[id]
    updateUserAsDict = updateUserIn.dict()
    for key in updateUserAsDict:
        value = updateUserAsDict[key]
        if value is not None:
            setattr(user, key, value)
    return user