from fastapi import FastAPI

app = FastAPI()

fakeDb = {
    0: "Bernard",
    1: "Joseph",
    2: "Kamala"
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    return fakeDb

@app.get("/users/{id}")
async def get_user(id: int):
    "Gets a user by id"
    user = fakeDb[id] 
    return user

@app.delete("/users/{id}")
async def delete_user(id: int):
    "Deletes an user by id"
    del fakeDb[id]