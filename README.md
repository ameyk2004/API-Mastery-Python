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