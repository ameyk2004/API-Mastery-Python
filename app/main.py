from random import randrange
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body

from pydantic import BaseModel
import time

import psycopg2
from psycopg2.extras import RealDictCursor

from . import utils

from . import schemas

from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from . import models

models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi_db", user="postgres", password="Amey1234", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection sucessful")
        break
    except Exception as error:
        print(f"Error {error}")
        print("Connection failed")
        time.sleep(2)


app = FastAPI()

@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}

@app.get('/posts')
def get_posts(db : Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"posts" : posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(title = post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"post" : new_post}

@app.get('/posts/{id}')
def get_post(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return {"post" : post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
  

@app.put('/posts/{id}')
def update_post(id: int, my_post: schemas.Post, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post.update({'title' : my_post.title, 'content': my_post.content, 'published' : my_post.published})

    db.commit()

    return {"status" : "success"}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    password = utils.hash(user.password)

    new_user = models.User(name=user.name, email=user.email, password=password,)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users')
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return {"users" : users}

@app.get('/users/{id}', response_model= schemas.UserOut)
def get_one_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Id {id} not found")

    return user
    

    