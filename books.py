import time
from fastapi import FastAPI
from datetime import date

from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import psycopg2

booksapp = FastAPI()

class bookdata(BaseModel):
    book_name :str
    name : str
    email : str
    borrow_date : date
    return_date : date


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='book_data', user='postgres',password='10may2005',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database was successfullly connected")
        break
    except Exception as error:
        print("connection to the database failed")
        print("the error was ",error)
        time.sleep(5)

@booksapp.post()
def add_book():

@booksapp

