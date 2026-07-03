from functools import total_ordering

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import datetime
from random import randrange
from pydantic_core.core_schema import none_schema

todo = FastAPI()


class note(BaseModel):
    title: str
    content: str
    created: datetime = datetime.now()


my_notes = []


@todo.get("/")
def homapage():
    print("welcome to my todo app")


@todo.post("/create")
def create_notes(new_note: note):
    notes_dict = new_note.dict()
    notes_dict['id'] = randrange(0, 100000)
    my_notes.append(notes_dict)

    return "note created successfully"


@todo.get("/posts")
def allposts():
    return {"data": my_notes}


def find(id):
    for n in my_notes:
        if n['id'] == id:
            return n


@todo.get("/post/{id}")
def get_postbyID(id: int, response: Response):
    note = find(id)
    if note == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found or does not exist"}
    else:
        return {"notes detail": note}
