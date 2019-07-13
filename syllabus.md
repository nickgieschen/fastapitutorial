# Syllabus

## Basic Python for this tutorial
Documentation [here](https://www.tutorialspoint.com/python/python_functions.htm)
<br>Quick lookup reference [here](https://www.w3schools.com/python/python_reference.asp)

- [dictionary](https://www.w3schools.com/python/python_dictionaries.asp)
- [tuple](https://www.w3schools.com/python/python_tuples.asp)
- [classes/objects](https://www.w3schools.com/python/python_classes.asp) 
- [class inheritance](https://www.w3schools.com/python/python_inheritance.asp)

## Basic Python one should know in general
- list
- tuple
- if
- for
- ranges
- functions
    - default args
    - keyword args
- classes/objects

## A little more advanced Python
- functions
    - variable lenth args
    - lambda 
- modules
- exceptions
- classes/objects
    - method overriding
    - information hiding with _ and __


## Web App
### Setup
We're going to set the project up as a pipenv managed project
- [docs](https://github.com/pypa/pipenv)
- Initialize the project as a pipenv managed project with `pipenv --python 3.7` (You can initialize with any Python version you'd like.) This will create a Pipfile, which is the file which contains your dependencies.
- Add a dependency. In this case, we're going to add FastAPI `pipenv install fastapi[all]`. In the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/intro/) they have `pip install fastapi[all]`. However, since we're using pipenv, we modify their installation instructions to use pipenv.
        
### Getting the server up and running
We're going to create our first route, then get the server running, and hit the route with our browser and Postman.
- [docs](https://fastapi.tiangolo.com/tutorial/first-steps/)
- Create a `main.py` file and write the first route as specified in the docs
- Start the webserver
    - `pipenv run uvicorn main:app --reload`. Again, the docs say you start the webserver with `uvicorn main:app --reload`, however since we're using pipenv we need to tell pipenv to run this command, hence we prefix it with `pipenv run`. The reason behind this is that by installing FastAPI (which includes uvicorn) with pipenv, we installed it to the virtual/local environment, not gloabally. So, if we had run the command in the FastAPI docs, our shell could not have found uvicorn. By prefixing the command with `pipenv run` we're saying "run this command from within the virtual environment" and it will work since we installed uvicorn to the virtual environment.
    - If you look on your command line, there were some logging statements when you started up the webserver. One of them tells you which IP the server was started on `INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`. Navigate to that in your web browser and it will execute the route we wrote for `/`.
- Hit the routes with Postman.<br>Eventually it's going to be easier to test our routes during development if we use Postman instead of our browser, so open up Postman and hit `/` with it.

### Basic routing
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

### Create and update routing the not so good way
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

### Create a create route the good way
Okay, now we're going to create our objects in a better way than in the section above. The code for this section is in a file called `main-3.py`. If you want to run it, use `pipenv run uvicorn main-3:app --reload`. 
- The first thing we have to do is delete (or comment out) the routes and functions we wrote in the last section, since we're going to doing them in a better way. So, remove `create-user` and `update-user`.
- Now we're going to create an update user route using the request body to send data to the server instead of a query string. FastAPI's docs on it are [here](https://fastapi.tiangolo.com/tutorial/body/)
    - First we need to import `BaseModel` from Pydantic with `from pydantic import BaseModel`. Keep in mind, that since Pydantic is a FastAPI dependecy, when we pip installed FastAPI, Pydantic got installed as well. So, we don't need to pip install it.
    - Now we're going to create a class which will represent the data coming in the body of the request. If you're following along in the FastAPI docs, note that this example will deviate a little from the FastAPI docs.
        ```python
        class UserIn(BaseModel):
            name: str
            age: str
            sex: str
        ```
        - We have inherited from `BaseModel`. This is necessary for us to use it to represent a request body in FastApi.
    - And now we'll create a route to handle the update.
        ```python
        @app.post("/users/")
        async def create_user(userIn: UserIn):
            user = User(userIn.name, userIn.sex, userIn.age)
            fakeDb[len(fakeDb)] = user
            return user
        ```
        (I'll explain what's going on in this function in a second. First we're going to hit it with Postman.)
    - Now we have to hit this route with Postman. To do that, we need to set up our call with a request body.
        - First, obviously, select the method as POST (remember it's in the dropdown to the left of the input where you enter the URL) and the URL `127.0.0.1:8000/users/`. 
        - Now we have to fill in the response body, so in Postman, below the URL input, in a tab which says "Body". Click on it and in the text field which appears write:
            ```json
            {
                "name": "Pete",
                "sex": "M",
                "age": 14
            }
            ```
        This is the data we are sending to the server.
        - Finally, we have to tell the server that our request body is json. That is, there are many formats we could have sent the request body in (XML, key/value, etc) and so we need to tell the server that we're sending JSON so the server knows how to parse what we're sending. Thus, under the Body tab, there is a radio button "raw". Click it and then select "JSON (application/json)" from the dropdown where it has probably defaulted to "Text". By doint this, we have told Postman to send a header called "content-type" along with our request with the value "application/json", which the server will read to determine that our body has been formatted as JSON.
        - Your Postman screen should look something like this:
        ![postman example](images/postman-1.png)
        - Now that we've set Postman up, we can hit our route. The result we see in Postman should be the new user we've created:
            ```json
            {
                "username": "Pete",
                "gender": "M",
                "age": 14
            }
            ```
    - Let's go back to the route we wrote again and look at what's going on.
        ```python
        @app.post("/users/")
        async def create_user(userIn: UserIn):
            user = User(userIn.name, userIn.sex, userIn.age)
            fakeDb[len(fakeDb)] = user
            return user
        ```
        - The first argument is of type UserIn. By doing this, we have told FastAPI to configure a route which will accept a request body in JSON of the form of the `UserIn` class. Namely, it should have `name`, `sex`, and `age` fields. And so this is what we sent in the request body. 
        - Just like we did with the query string data in the previous section, we're creating a new User object, but this time with the data from the request body.
        - Finally, we are adding the user to our fake database (a little more succcintly this time)

### Create an update route the good way
Now, with code very similar to the last section, we're going to create a route to update our object. The code for this section is in a file called `main-4.py`. If you want to run it, use `pipenv run uvicorn main-4:app --reload`. This section will show you how to update an object in a basic way. In the FastAPI documentation they show [similar, but slightly more succinct](https://fastapi.tiangolo.com/tutorial/body-updates/) ways to do the same thing. I'm not using their method here, since I think it's clearer to show it this way and then add in the FastAPI magic one you understand what's going on in this code.
- First we're going to create an `UpdateUserIn` model, similar to the `UserIn` model we created above:
    ```python
    class UpdateUserIn(BaseModel):
        username:str = None
        gender:str = None
        age:int = None
    ```
    Note that this class is very similar to the UpdateUser class in the previous section. The difference here is that we've given each property a default value of `None`. What this does is that it tells FastAPI that each of the properties with a default value is optional. The reason this is necessary is that, since we're updating a user, we may want to update only one property. In other words, the JSON we send in our request might look something like this if we just want to update the user's age:
    ```json
    {
        "age": 22
    }
    ```
    If we hadn't given the other two properties `username` and `gender` a default value, thereby making them optional, FastAPI would have thrown an error since they weren't included in the body of our request.
- We now create our route:
    ```python
    @app.patch("/users/{id}")
    async def update_user(updateUserIn: UpdateUserIn, id: int):
        user = fakeDb[id]
        updateUserInAsDict = updateUserIn.dict()
        for key in updateUserInAsDict:
            value = updateUserInAsDict[key]
            if value is not None:
                setattr(user, key, value)
        return user
    ```
    A couple things to observe:
    - We're using `PATCH` as our HTTP method, since we're updating an existing user. 
    - We're using both [path parameters](https://fastapi.tiangolo.com/tutorial/path-params/) and [request body](https://fastapi.tiangolo.com/tutorial/body/) in our function signature.
    - Let's parse out what's going on with:
        ```python
        updateUserInAsDict = updateUserIn.dict()
        for key in updateUserAsDict:
            value = updateUserAsDict[key]
            if value is not None:
                setattr(user, key, value)
        ```
        - In short, we are looping over the key/value pairs in our request body. If the value is not `None` we set the attribute we sent in the request on the user object we retrieved from the fake database with the value we passed in the request. Now a little more explanation:
            - We need to loop over the items we sent in the request body. For example, if we want to update both the age and gender, our request body would look like:
            ```json
            {
                "age": 33,
                "gender": "F"
            }
            ```
            So, we want to loop over this structure. In the first iteration of the loop, we'll set the age to 33 and in the second iteration of the loop we'll set gender to F. We can't loop through the properties of an object, but we can loop through a dictionary. So, we use the `dict()` method of [Pydantic's BaseModel](https://github.com/samuelcolvin/pydantic/blob/master/pydantic/main.py) since that returns the properties and the values of an object as a dictionary. (Since `UpdateUserIn` inherits from `BaseModel`) this method can be called on `UpdateUserIn`. So, now `updateUserInAsDict` is a dictionary containing the key/value pairs of `UpdateUserIn`.
            - `for... in` on a dictioary loops over the keys of a dictioary.
            - We extract the value at the key with `value = updateUserAsDict[key]`.
            - Keep in mind, the dictionary at this point includes *all* of the properties of the UpdateUserIn model. So, the ones we *didn't* set in the JSON we passed in in the body of our request are still present, but they are set to none. In other words, if the JSON in our request was:
            ```json
            {
                "age": 33,
            }
            ```
            The dictionary of updateUserAsDict will be:
            ```python
            {
                username = None,
                age = 33,
                gender = None 
            }
            ```
            So, in order to not set the values on our user object to `None`, we use an if clause to make sure they are not `None`.
            - Once we make sure they are not `None`, we set the appropriate property on the user object to the appropriate value.




### TODO
- Split out code to modules
- Breakpoint
- Request body & pydantic
- Create a unit test for each route
- Docs for unit tests
- Run the unit tests
    - on commandline
    - in VSCode 
    - Start with a simple class
    - Find docs
    - Use pip to install Gino dependency
    - Get started with Gino/SqlAlchemy
    - Create models
    - Build DB
    - Use a route to 
        - create a model
        - read a model
        - update a model
        - delete a model

- #### Test routes with models
    - Set up dummy data
    - Mock out DB calls

- ## Git
    - Branch
    - Merge
    - Resolve conflicts
