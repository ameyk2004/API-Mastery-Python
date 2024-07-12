from fastapi import FastAPI
from fastapi.params import Body
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine
from . import models
from .routers import posts, users

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

app.include_router(posts.router)
app.include_router(users.router)

@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}

