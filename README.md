# API Mastery Python

This repository is dedicated to mastering `API development` using Python, covering key technologies such as FastAPI for efficient API building, SQL and `PostgreSQL` for robust database management, Docker for containerization, and deployment on AWS for scalable production environments. Join me on this journey to build a solid foundation in API development from start to finish.

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [FastAPI Introduction](#fastapi)
- [GET and POST Requests with FastAPI](#get-request-with-fastapi)
- [CRUD operations in FastAPI](#crud-operations-in-fastapi)
- [FastAPI Routers](#fastapi-routers)
- [ORM (Object Relational Mapper)](#orm-object-relational-mapper)
- [SQLAlchemy](#sqlalchemy)
- [ORM models Vs Pydantic models](#orm-models-vs-pydantic-models)
- [Authentication and User Model](#authentication-and-user-model)
- [Password Security using Hashing](#password-security-using-hashing)
- [JWT Token Authentication](#jwt-token-autentication)
- [Login Process Using JWT](#login-process-using-jwt)

## Introduction

This project aims to provide a comprehensive guide to API development with Python, starting from the basics and progressing to more advanced topics. By following along, you'll gain hands-on experience with modern API development practices and tools.

## Technologies Used

<div style="display: flex; align-items: center; gap: 15px;">
    <img src="https://seeklogo.com/images/F/fastapi-logo-541BAA112F-seeklogo.com.png" height="70" alt="FastAPI">
    <img src="https://cdn-icons-png.flaticon.com/512/4492/4492311.png" height="70" alt="Icon">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1985px-Postgresql_elephant.svg.png" height="70" alt="PostgreSQL">
    <img src="https://cdn.iconscout.com/icon/free/png-256/free-docker-226091.png?f=webp&w=256" height="60" alt="Docker">
    <img src="https://www.pngall.com/wp-content/uploads/13/AWS-Logo-PNG-File.png" height="70" alt="AWS">
</div>



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

- keep your pydantic models in `schemas.py` file.

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

## FastAPI Routers

- if you have two manage the routes in your application which are related you can use APIRouter
- create a file structure to store `/posts` routs  and `/users` routes in different directories.

```
└── app
    ├── __init__.py
    └── routers
        ├── posts.py
        ├── users.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

- Your `posts.py` or `users.py` should look like this.

```python
from fastapi import APIRouter

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)

@router.get('/')
def get_posts(db : Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"posts" : posts}
```

- include this routes to app in `main.py`

```python
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
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

## `SQLAlchemy`

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

## ORM models Vs Pydantic models

<img src="assets/Screenshot 2024-07-10 at 8.31.48 AM.png">

<img src="assets/Screenshot 2024-07-10 at 8.33.02 AM.png">


## Authentication and User Model

- basically we will just cretate a UserCreate Model and UserOut model (pydantic) to validate creation and response of our user 

`schemas.py`

```python
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
```

Now you should be able to perform normal `CRUD` operations with users

### CRUD with Users

```python
#create
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(name=user.name, email=user.email, password=user.password,)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#read
@app.get('/users')
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return {"users" : users}
```
## Password Security using Hashing

### Why Use Hashing for Passwords?
Hashing passwords adds a layer of security to stored passwords, making it difficult for unauthorized users to retrieve them. Instead of storing the actual passwords, applications store the hashed version of the passwords. Even if an attacker gains access to the stored data, they only get the hashed values, not the actual passwords.

### Hashing Algorithms
There are various hashing algorithms available, such as:

- `MD5`: Message Digest Algorithm 5, though it is not recommended due to vulnerabilities.
- `SHA-1`: Secure Hash Algorithm 1, which is also now considered insecure for sensitive data.
- `SHA-256`: Part of the SHA-2 family, it is widely used and considered secure.
- `bcrypt`: Specifically designed for hashing passwords, it includes a work factor to adjust the algorithm’s complexity.

### Salting

Salting is a technique used to enhance password security. A salt is a random value added to the password before hashing. This ensures that even if two users have the same password, their hashed values will be different.

### Implimentaion

- Install the `passlib` library for password hashing

```bash
pip install passlib
pip install bcrypt
```

- Create a `utils.py` file to store password Hashing Logic

```py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)
```

## JWT Token Autentication

<img src="assets/Screenshot 2024-07-12 at 10.10.32 AM.png">


### 1. Login Request
- **Action**: The client sends a login request to the API endpoint.
- **Data**: This request includes the user's credentials, typically a username and password.
- **Endpoint**: /login (username + password)

### 2. Credentials Verification
- **Action**: The API verifies the provided credentials.
- **Condition**: If the credentials are valid, the API generates and signs a JWT token.
- **Token Generation**: The token is created using the user's information and a secret key.

### 3. Token Response
- **Action**: The API sends the JWT token back to the client.
- **Data**: The client receives the token, which contains encoded user information and signature.

### 4. Authenticated Request
- **Action**: The client makes a subsequent request to a protected endpoint.
- **Data**: This request includes the JWT token in the headers.
- **Endpoint**: /posts {token}

### 5. Token Validation
- **Action**: The API verifies the validity of the token.
- **Verification Steps**:
    - *Signature Verification* : Ensures the token hasn't been tampered with.
    - *Expiration Check* : Verifies that the token hasn't expired.

### 6. Data Response
- **Action**: If the token is valid, the API processes the request and sends the requested data back to the client.
- **Data**: The client receives the data.

<img src="assets/Screenshot 2024-07-12 at 10.22.41 AM.png">

<img src="assets/Screenshot 2024-07-12 at 10.29.05 AM.png">


- PLEASE DO NOT PROCEED UNLESS YOU HAVE UNDERSTOOD WHY THE SIGNATURE IS IMPORTANT


## Login Process Using JWT

- create your login router and return a created token

- install these dependencies 

```bash
pip install python-jose
```

- Create a file named `oath2.py`

```python
@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email Not Found")
    
    verifcation = utils.verify(user_credentials.password, user.password)

    if not verifcation:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect Password")

    access_token =  oath2.create_access_token({"id" : user.email})

    return {"access_token" : access_token, "token_type" : "bearer"}  
```
