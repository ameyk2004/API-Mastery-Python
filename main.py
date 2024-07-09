from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
def root():
    return {"message" : "Hello from FastAPI"}

@app.get('/posts')
def get_posts():
    return {"data" : "These are your posts"}

@app.post('/create-post')
def create_post(payload: dict=Body(...)):
    return {"new post" : f"Created post with {payload}"}