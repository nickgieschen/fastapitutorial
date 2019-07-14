## Web App Setup

### Pipenv
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