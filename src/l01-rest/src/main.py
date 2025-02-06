from fastapi import FastAPI
from pydantic import BaseModel

class Pessoa(BaseModel):
    nome: str
    sobrenome: str
    idade: int

app = FastAPI()

counter = 0

@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/count")
def get_count():
    global counter
    counter += 1
    return counter

@app.get("/hello")
def hello_world():
    return "Hello, anonymous"

@app.get("/hello/{name}")
def hello(name):
    return f"Hello, {name}"

@app.get("/hello/")
def hello(parameter = "World"):
    return f"Hello, {parameter}"

@app.post("/pessoa/")
def criar_pessoa(pessoa: Pessoa):
    return pessoa
