## Create and Update Routes the not so Good Way
Now we're going to create some routes to create and update items in our database. The code for this section is in a file called `main-2.py`. If you want to run it, use `pipenv run uvicorn main-2:app --reload`. This section is going to be a bit of a contrived example and does not represent best practices. However, it's useful for two reasons: (1) We get to practice using query strings with routes and (2) it represents a good stepping stone to the next section where we incorporate Pydantic and models.

- First we're going to change our database so it contains objects instead of strings.
    - First we have to create a `User` class. To good tutorial on basics of classes is [here](https://www.w3schools.com/python/python_classes.asp)
        ```python
        class User:
            def __init__(self, username, gender, age):
                self.username = username
                self.gender = gender
                self.age = age
        ```
    - Next we declare our database as a dictionary and then create users and add them to the dictionary
        ```python
        fakeDb = {}

        fakeDb[0] = User("Joe", "M", 78)
        fakeDb[1] = User("Kamala", "F", 55)
        fakeDb[2] = User("Bernard", "M", 76)
        ```
    - If we hit `/users` now with a GET request with Postman (the route which responds with our database) we can see all of the users we've created. 
- Now we're going to create a route to create a user. For this example, we're going to use [query params](https://fastapi.tiangolo.com/tutorial/query-params/) to pass data to the server. Typically we'd use [request body params](https://fastapi.tiangolo.com/tutorial/body/), but that's a bit more complicated and we'll tackle that in the next section. 
    - We are going to create a route which will accept a URL which looks like `127.0.0.1:8000/create-user?username=Elizabeth&gender=F&age=77`. In this URL, the key/value pairs after the `?` are called query string parameters and are one way we can pass data from the client to the server. In other words, in our server side code we can read those key/value pairs and do something with them.
    - Our route to handle a URL like this will look like this:
        ```python
        @app.get("/create-user/")
        async def create_user_query_string(username: str, gender: str, age: int):
            user = User(username, gender, age)
            nextId = len(fakeDb)
            fakeDb[nextId] = user
        ```
        Observe a few things from the code above:
        - As per the FastAPI docs, the parameteres in the query string map to the arguments of the function.
        - We use the query string parameters to create a `User` object
        - We use the `len` function to get the length of the `fakeDb` dictionary, which we will use as our key for this user.
    - Now we're going to hit this route in Postman with `127.0.0.1:8000/create-user?username=Elizabeth&gender=F&age=77` and then verify it worked by inspecting our database with `127.0.0.1:8000/users`
- Next, we're going to create a route to update an existing item in our database. 
    - Again we're going to use a query string to do this, though we'll refactor to a better way in the next section. For now, the query string we'll use is `127.0.0.1:8000/update-user?id=1&prop=gender&value=M`. This URL tells the server via the query string that we want to updage the user with the `id` of 1 and our update will update the property `age` with the value 55.
    - Now we define a route to handle such a URL
        ```python
        @app.get("/update-user")
        async def update_user_query_string(id: int, prop: str, value: str):
            user = fakeDb[id]
            setattr(user, prop, value)
        ```
        Observe the following about the above function:
        - We are retrieving the user from the dictonary by using the value in the `id` param
        - We are using python's [setattr](https://www.w3schools.com/python/ref_func_setattr.asp) built-in function to set the attribute passed in the query string to the value passed in the query string.
    - Now we're going to hit this route in Postman with `127.0.0.1:8000/update-user?id=1&prop=gender&value=M` and then verify it worked by inspecting our database with `127.0.0.1:8000/items`. Now Kamala's gender should be M.
    - Next, we have to fix a subtle bug we've introduced. 
        - To see the bug, we're first going to view non-buggy data. To do so, retrieve one of the users with `127.0.0.1/users/1`. The result should look something like this:
            ```python
            {
                "username": "Kamala",
                "gender": "M",
                "age": 55
            }
            ```
        - Now lets update that user's age with `127.0.0.1:8000/update-user?id=1&prop=age&value=45` and retrieve the user again. Now they'll look like:
            ```python
            {
                "username": "Kamala",
                "gender": "F",
                "age": "45"
            }
            ```
            See the bug? Before setting the age, the age was represented correctly as an integer. Now, however, age is represented as a string. This is because in our `update_user_query_string` method we declared `value` as a `str`. So, give some thought as to how you'd fix this. [Docs on casting](https://www.w3schools.com/python/python_casting.asp) and [docs on if statements](https://www.w3schools.com/python/python_conditions.asp) might help.