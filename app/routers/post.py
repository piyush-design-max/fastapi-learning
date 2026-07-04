from fastapi import  Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"status": "success"}


@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select*from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning*""",
    #                (new_post.title, new_post.content, new_post.publish))
    # # we use %s to prevent sql injection ie someone can pass a sql code into it and which can manipulate out database so % kinda sanitizes it.
    # postz = cursor.fetchone()
    # conn.commit()

    postz = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    db.add(postz)
    db.commit()
    db.refresh(postz)

    # this postz is a sqlalchemy model/object
    # and sqlalchemy model cannot be converted to dict(), pydantic model only has the dict() option so you need to used config thing
    return postz


# def find_index(id):
#     for i in range(0, len(my_posts)):
#         if my_posts[i]["id"] == id:
#             return i
#     # alternate method
#     # for index,p in enumerate(my_posts):
#     #     if p["id"]==id:
#     #         return index


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    # cursor.execute("""select*from posts where id = %s""", (str)(id))
    # testpost = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found"}
    return post


# title str, content str, category, bool published
@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # # deleting post
    # # finding the data of that id
    # # mypost.pop(index)
    # cursor.execute("""delete from posts where id = %s returning*""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.Post):
#     # cursor.execute("""update posts set title = %s,content = %s, published = %s where id = %s returning*""",
#     #                (post.title, post.content, post.publish, str(id)))
#     # updated_posts = cursor.fetchone()
#     # conn.commit()
#
#     # if updated_posts == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
#     #
#     # return updated_posts
