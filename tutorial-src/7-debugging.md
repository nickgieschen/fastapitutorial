## Debugging
We're going to take a quick tour to set up some advanced debugging tooling so we don't have to scatter `print` statements all over our code when we need to inspect it. The code for this section is in `main-5.py`.
- Follow the instructions on setting the app up for debugging [here](https://fastapi.tiangolo.com/tutorial/debugging/). A few observations:
    - Make sure you put the following code at the *bottom* of your main file so that the `FastAPI` object (`app`) has completed it's initialization by the time it's passed to `uvicorn.run`.
    ```python
    if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    ```
    - You can set the IP in `uvicorn.run` to anything you'd like. Since we've been using `127.0.0.1` in this tutorial, I've set it to that. 
    - If you get an error which states that "address is already in use", it means that something else is trying to run on the IP you chose to run uvicorn on. It's probably another FastAPI instance you have running. Shut that instance down and then try again.
- Now we're going to set up VSCode to run the app instead of starting it our terminal. The reason we want VSCode to start the app up is that then it can set up the debugger which allows us to use VSCode's advanced debugging tools. Below is a short video showing how to configure VSCode to start the debugger and, once your app is running, how to set breakpoints in order to inspect the code:
 <video controls style="width: 100%">
  <source src="../images/debugging.mp4" type="video/mp4">
</video> 
