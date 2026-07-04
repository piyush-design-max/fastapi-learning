from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth
models.Base.metadata.create_all(bind=engine)

# creating a app object of fastapi just like in java
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



# the get method fetches data from the api server not the html webpage
@app.get("/")
def root():
    return {"message": "hello world welcome to my api"}



