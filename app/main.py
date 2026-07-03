from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import psycopg2
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# creating a app object of fastapi just like in java
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='10may2005',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break

    except Exception as error:
        print("connection to database failed")
        print("the error was ", error)
        time.sleep(2)

my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1},
            {"title": "title of post2", "content": "content of post 2", "id": 2}]


# the get method fetches data from the api server not the html webpage
@app.get("/")
def root():
    return {"message": "hello world welcome to my api"}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"status": "success"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select*from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning*""",
    #                (new_post.title, new_post.content, new_post.publish))
    # # we use %s to prevent sql injection ie someone can pass a sql code into it and which can manipulate out database so % kinda sanitizes it.
    # postz = cursor.fetchone()
    # conn.commit()

    postz = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    db.add(postz)
    db.commit()
    db.refresh(postz)

    return {"data": postz}


def find_index(id):
    for i in range(0, len(my_posts)):
        if my_posts[i]["id"] == id:
            return i
    # alternate method
    # for index,p in enumerate(my_posts):
    #     if p["id"]==id:
    #         return index


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""select*from posts where id = %s""", (str)(id))
    testpost = cursor.fetchone()
    print(testpost)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found"}
    return {"post detail": testpost}


# title str, content str, category, bool published
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # finding the data of that id
    # mypost.pop(index)
    cursor.execute("""delete from posts where id = %s returning*""", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""update posts set title = %s,content = %s, published = %s where id = %s returning*""",
                   (post.title, post.content, post.publish, str(id)))
    updated_posts = cursor.fetchone()
    conn.commit()

    if updated_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return {"message": updated_posts}
