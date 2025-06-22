from typing import Optional
from pydantic import BaseModel


class CreateUser(BaseModel):
    """
    Helper class to create a request body for the user creation
    """
    username: str

class CreateTodo(BaseModel):
    """
    Helper class to create todos with request body
    """
    user_id: int
    title: str
    body: Optional[str]

class UpdateTodo(BaseModel):
    """
    Helper Class to update todos
    """
    title: Optional[str]
    body: Optional[str]