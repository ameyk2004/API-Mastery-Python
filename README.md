# API-Mastery-Python

This repository is dedicated to mastering `API development` using Python, covering key technologies such as FastAPI for efficient API building, SQL and `PostgreSQL` for robust database management, Docker for containerization, and deployment on AWS for scalable production environments. Join me on this journey to build a solid foundation in API development from start to finish.

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)

## Introduction

This project aims to provide a comprehensive guide to API development with Python, starting from the basics and progressing to more advanced topics. By following along, you'll gain hands-on experience with modern API development practices and tools.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **SQL**: Structured Query Language for database interaction.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **AWS**: Amazon Web Services, a comprehensive cloud computing platform.

## Setup and Installation

### Make your own Virtual enviornment

```bash
python3 -m venv venv
```

### Select Your Virtual Environment (VS Code):

- Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux) to open the command palette.
- Type Python: Select Interpreter and select the virtual environment you created (it should show a path ending with venv).

### Activate the Virtual Environment:

```bash
source venv/bin/activate
```

### Install Fast API
- [FastAPI Documentation](https://fastapi.tiangolo.com)

```bash
pip install fastapi
```

## FastAPI

- to get upp and running copy the code below to create a simple `GET API`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}
```

- Run your server

```bash
uvicorn main:app
```

The above command runs your `main.py` file on a server at port 8000 but any changes dont reflect uless the server is stopped and restarted

so during development we can use 

```bash
uvicorn main:app --reload
```

### GET Request with FastAPI

GET requests are used to retrieve data from a server. To handle a GET request in FastAPI, use the @app.get decorator.

Here's an example of a simple GET request:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

In this example:

- The read_root function handles GET requests to the root URL (/).
- The read_item function handles GET requests to /items/{item_id}, where item_id is a path parameter.


### POST Requests in FastAPI

POST requests are used to send data to a server to create or update a resource. To handle a POST request in FastAPI, use the @app.post decorator.

Here's an example of a simple POST request:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}

```

In this example:

- A Pydantic model Item is defined to validate the request body.
- The create_item function handles POST requests to /items/. It expects a JSON body that matches the Item model and returns the received item.

<hr>

# CRUD operations in FastAPI

<img src="assets/Screenshot 2024-07-09 at 10.46.38 AM.png">

```python
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

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    post_dict = dict(post)
    post_dict["id"] = id

    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    my_posts[index] = post_dict
    
    return {"message" : "updated"}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    print(index)

    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    my_posts.pop(index)
```

## PostgreSQL Integration

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1985px-Postgresql_elephant.svg.png" width=100>

### Adaptaer for Python `Psycopg`

- [Psycopg Docs](https://www.psycopg.org/docs/)
- Visit the docs to Connect Postgresql with Python

```python
#code below should run after a sucessful connection

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

# This is good for development Environment
# dont rely on this if deployment server
```
## ORM (Object Relational Mapper)

- Layer of abstraction that sits between the database and us.
- Now we dont need to fire raw sql commands directly we can talk to our `ORM` with python code.

<img src="assets/Screenshot 2024-07-09 at 8.45.54 PM.png">

<img src="assets/Screenshot 2024-07-09 at 8.48.14 PM.png">

- One of the most Popular ORM tool is SQLAlchemy

## `SQLAlchemy` - ORM

- this is a standalone library
- Nothing to do with `FastAPI`
- ORMS cant directly talk to database you need drivers so ru these import statements

```bash
pip install sqlalchemy
pip install psycopg2-binary
```

Create a folder structure similar to below:

```.
└── app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

- `database.py` should contain the sqlAlchemy initializations like below

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"
# Example : SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Amey1234@localhost/fastapi_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- `models.py` should contain your tables

```python
from sqlalchemy import VARCHAR, Boolean, Column, Integer
from .database import Base 

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(VARCHAR, nullable=False)
    published = Column(Boolean, default=True)  
```

- Your `main.py` file should like below

```python
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

@app.get('/sqlalchemy')
def test(db: Session = Depends(get_db)):
    pass

```