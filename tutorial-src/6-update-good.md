## Update Routes the Good Way
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