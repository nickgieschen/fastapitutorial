## Read and Delete Routes

For this we're going to create a fake database and create some read and delete routes to manipulate the data in the fake database. The code for this section is in a file called `main-1.py`. If you want to run it, use `pipenv run uvicorn main-1:app --reload`. 
- We start by creating a fake database, which will just be a dictionary:
    ```python
    fakeDb = {
        0: "Bernard",
        1: "Jospeh",
        2: "Kamala"
    }
    ```
- Now we're going to create a route which will return the entire database. This way we can check it after each CRUD operation to make sure we've manipulated it in the way we intended:
    ```python
    @app.get("/users")
    async def get_users():
        return fakeDb
    ```
- Now we hit this with postman by going to `127.0.0.1/users` and we should get our fakeDb in the response.
- Now lets create a "read" route. 
    ```python
    @app.get("/users/{id}")
    async def get_user(id: int):
        "Gets a user by id"
        item = fakeDb[id] 
        return item
    ```
    Observe a few things in the code above:
    - The path parameter defined in the route gets passed to the function.
    - The first line in a python function, if it's a string, will be used as documentation for the function.
    - We retrieve an item from a python [dictionary](https://www.w3schools.com/python/python_dictionaries.asp) with `dict[key]` syntax.
    - Check the [docs](https://fastapi.tiangolo.com/tutorial/path-params/) for more info on path parameters.
- Now we hit this with postman by going to `127.0.0.1/users/1` and we should get "Joseph" as the response.
- Now lets create a "delete" route:
    ```python    
    @app.delete("/users/{id}")
    async def delete_user(id: int):
        "Deletes a user by id"
        del fakeDb[id]
    ```
    - We have defined the route as a "delete" route. That is, is order to hit that route our request has to specify that the HTTP method is "DELETE". (We'll see how to do this in Postman in the next step.)
    - We're using the `del` keyword to [remove the item at the key specified](https://www.w3schools.com/python/python_dictionaries.asp). As the docs show, we could also have written `fakeDb.pop(id)`.
- Now we're going to hit this route with Postman. In order to do so, we have to specify the path as `127.0.0.1/users/1`. However, to the left of where we specify the path there is a dropdown which specifies the HTTP method. At the moment, it is probably populated with GET. Change it to DELETE and then click "Send". The server will see that the HTTP method is DELETE and select our delete route to run. Since we're not returning anything from the delete route, we won't see anything in Postman which will indicate that the item got deleted. In order to check whether the item got deleted, we now hit the route which returns our entire fake database. We should see that item 1 is no longer in there.