from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
import time

import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        connection = psycopg2.connect(host="localhost", database="fastapi_db", user="postgres", password="Amey1234", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
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

my_posts = [
    {
        "title" : "Title 1",
        "content" : "Content 1",
        "id" : 1
    },
    {
        "title" : "Title 2",
        "content" : "Content 2",
        "id" : 2
    },
]

def find_post(id : int):
    for post in my_posts:
        if post["id"] == id:
            return post
        

def find_post_index(id : int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i

@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}

@app.get('/posts')
def get_posts():
    return {"posts" : my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    id = randrange(0,100000)

    post_dict = dict(post)
    post_dict["id"] = id

    my_posts.append(post_dict)
    return {"post" : post_dict, "status" : "success"}

@app.get('/posts/{id}')
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {"post" : post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    print(index)

    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    my_posts.pop(index)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    post_dict = dict(post)
    post_dict["id"] = id

    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    my_posts[index] = post_dict
    
    return {"message" : "updated"}
