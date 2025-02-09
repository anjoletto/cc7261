# Lab 01 - REST usando FastAPI

## Instalação

### *NIX (Linux, macOS, BSD,...)
```sh
python -m venv .venv
```

```sh
source .venv/bin/activate
```

```sh
pip install "fastapi[standard]"
```
ou

```sh
pip install -r requirements.txt
```

### Windows dos laboratórios

```sh
pip install --user fastapi uvicorn
```

## Para testar

No arquivo `main.py` adicione:
```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}
```

No terminal, se for *NIX:
```sh
fastapi dev main.py
```

Se for laboratório usando Windows:
```sh
python -m uvicorn main:app --reload
```


No browser abra as páginas:
- http://localhost:8000/
- http://localhost:8000/docs
- http://localhost:8000/redocs

Adicione no arquivo `main.py` um contador `i` inicializado com zero e a seguinte função:
```py
@app.get("/count")
def get_count():
    global counter
    counter += 1
    return counter
```

Acesse http://localhost:8000/count e atualize a página algumas vezes.
1. O que acontece com o contador?
2. Por que é necessário declarar a variável `counter` como global?
3. Por que esta função não respeita a arquitetura REST?

## Métodos HTTP

| uso                 | HTTP    | fastapi         |
| ------------------- | ------- | --------------- |
| para receber dados  |`GET`    | `@app.get()`    |
| para criar dados    |`POST`   | `@app.post()`   |
| para atualizar dados|`PUT`    | `@app.put()`    |
| para deletar dados  |`DELETE` | `@app.delete()` |


### Método `GET` e paths

Adicione as seguintes funções no arquivo `main.py` e teste o seu uso:

```py
@app.get("/hello")
def hello_world():
    return "Hello, world"
```

```py
@app.get("/hello/{name}")
def hello(name):
    return f"Hello, {name}"
```

```py
@app.get("/hello/")
def hello(parameter = "World"):
    return f"Hello, {parameter}"
```

Qual a diferença entre eles?

### `POST`

No arquivo `main.py` importe o `BaseModel` do `pydantic` e adicione os seguintes códigos ao arquivo `main.py`
```py
class Pessoa(BaseModel):
    nome: str
    sobrenome: str
    idade: int
```

```py
@app.post("/pessoa/")
def criar_pessoa(pessoa: Pessoa):
    return pessoa
```

Teste a execução do `POST` usando o Swagger ou com o `curl` executando
```sh
curl -X 'POST' 'http://localhost:8000/pessoa/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "nome": "Nome", "sobrenome": "Sobrenome", "idade": 1 }'
```

## Exemplo um pouco mais longo

Teste o código a seguir e descreva o que cada função está fazendo (comente no próprio código)

```py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tarefas = list()

class Tarefa(BaseModel):
    tarefa: str
    prioridade: int
    feito: bool

@app.get("/")
def root():
    return tarefas


@app.get("/tarefa/{pos}")
def get_tarefa(pos: int):
    return tarefas[pos]

@app.post("/adicionar/")
def criar_tarefa(tarefa: Tarefa):
    tarefa.feito = False
    tarefas.append(tarefa)
    return len(tarefas)

@app.put("/feito/{pos}")
def marcar_feito(pos: int):
    tarefas[pos].feito = True
    return tarefas[pos]

@app.delete("/deletar/{pos}")
def deletar_tarefa(pos: int):
    tarefa = tarefas.pop(pos)
    return tarefa
```

Utilize o Swagger para testar as chamadas de cada recurso implementado.

## Exercício

Usando o FastAPI, implemente um serviço para gerenciar uma lista de contatos.
