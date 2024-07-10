from random import randrange
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body

from pydantic import BaseModel
import time

import psycopg2
from psycopg2.extras import RealDictCursor

from app.schemas import Post

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
def create_post(post: Post, db: Session = Depends(get_db)):
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
def update_post(id: int, my_post: Post, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post.update({'title' : my_post.title, 'content': my_post.content, 'published' : my_post.published})

    db.commit()

    return {"status" : "success"}


