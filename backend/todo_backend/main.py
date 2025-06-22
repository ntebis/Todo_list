from fastapi import FastAPI, HTTPException

from todo_backend.database import Database
from fastapi.middleware.cors import CORSMiddleware

db = Database()

app = FastAPI(docs_url = "/")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# status code 201 since it creates a new user
@app.post("/user/", status_code=201)
def create_user(username: str) -> int:
    """
    Endpoint to create a user

    Args:
        username (str): The username selected

    Returns:
        int: The user id of the created user
    """
    res = db.create_user(username)

    if res != -1:
        return res
    elif res == -1:
        raise HTTPException(status_code=409, detail=f"User {username} Exists")
    else:
        raise HTTPException(status_code=500)


@app.get("/user/")
def get_user(username: str) -> int:
    """
    Get the user id from a username

    Args:
        username (str): The username

    Returns:
        int: The user id
    """
    res = db.get_user_id(username)
    if res != -1:
        return res
    else: 
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    

@app.get("/user/{user_id}/notes")
def get_all_notes_for_user(user_id: int) -> list[dict]:
    """
    Get all the notes associated to a user

    Args:
        user_id (int): The user id of the user

    Returns:
        list[dict]: List of json objects of all the user notes
    """
    res = db.get_all_notes(user_id)
    if res:
        return res
    else:
        raise HTTPException(status_code=204, detail=f"No notes were found for user_id {user_id}")

@app.post("/todo/", status_code=201)
def create_todo(user_id: int, title: str, body: str = None) -> dict:
    """
    Create a todo note

    Args:
        user_id (int): The user_id of the user that is creating the note
        title (str): The title of the note
        body (str, optional): Any additional contents for the note. Defaults to None.

    Returns:
        dict: JSON object of the note added
    """
    todo_id = db.create_todo(user_id, title, body)
    return db.get_single_todo(todo_id)


@app.get("/todo/{todo_id}")
def get_todo(todo_id: int) -> dict:
    """
    Get a todo note

    Args:
        todo_id (int): The id of the note

    Returns:
        dict: JSON object of the note
    """
    note = db.get_single_todo(todo_id)

    if note:
        return note
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} was not found")


@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, title: str = None, body: str = None) -> dict:
    """
    Update a todo note

    Args:
        todo_id (int): The id of the note
        title (str, optional): The modified title of the note. Defaults to None.
        body (str, optional): the modified body of the note. Defaults to None.

    Returns:
        dict: JSON object that contains the modified note
    """
    res = db.update_todo(todo_id, title, body)

    if res != -1:
        return db.get_single_todo(todo_id)
    elif res == -1 :
        raise HTTPException(status_code = 304, detail = f"Todo with id {todo_id} was not modified")


@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int) -> dict:
    """
    Delete a todo note

    Args:
        todo_id (int): The id of the note

    Returns:
        dict: JSON object of the deleted note
    """
    note = db.get_single_todo(todo_id)

    if note:
        db.delete_todo(todo_id)
        return note
    else:
        raise HTTPException(status_code = 404, detail=f"Todo with id {todo_id} was not found")
    
