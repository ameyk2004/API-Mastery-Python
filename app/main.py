from random import randrange
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body

from pydantic import BaseModel
import time

import psycopg2
from psycopg2.extras import RealDictCursor

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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts" : posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    
    try:
        cursor.execute(
            "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)",
            (post.title, post.content, post.published)
        )
        conn.commit()

    except Exception as error:
        return {"error" : f"{str(error)}"}
    
    return {"status" : "success"}

@app.get('/posts/{id}')
def get_post(id:int):
    try:
        cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
        got_post = cursor.fetchone()
        print(got_post)

        if got_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
        
        return {"post" : got_post}
    
    except HTTPException as http_error:
        return http_error
    
    except Exception as error:
        return {"error" : str(error)}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
        post = cursor.fetchone()

        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
        
        cursor.execute(f"DELETE FROM posts WHERE id = {id}")
        conn.commit()

    except HTTPException as http_error:
        return http_error
    
    except Exception as error:
        return {"error" : str(error)}

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    try:
        cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
        got_post = cursor.fetchone()
        cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",(post.title,post.content,post.published,id))

        if got_post == None:
            raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
        conn.commit()
        return {"status" : "success"}
    
    except HTTPException as http_error:
        return http_error
    
    except Exception as error:
        return {"error" : str(error)}


@app.get('/sqlalchemy')
def test(db: Session = Depends(get_db)):
    pass
