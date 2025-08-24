# Exercício 2: Acesso externo em endpoints disponíveis dentro do container

Neste exercício vamos juntar o que foi implementado na primeira aula de laboratório com o que vimos no exercício anterior. O resultado final será a execução de um container com os endpoints desenvolvidos usando FastAPI sendo acessados de fora do container junto com a execução de 10 containers que geram valores aleatórios.

## Container com FastAPI

O código usado neste exercício é o mesmo da primeira aula e para facilitar, encontra-se a seguir:

```python
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

Para que este código possa ser executado de dentro de um container, vamos usar um `Dockerfile` que copia o arquivo com o código, instala as dependências necessárias e executa o FastAPI quando o container é inicializado.

```Dockerfile
FROM python:3.13.7-alpine3.21

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
```

O `Dockerfile` desenvolvido usa a mesma imagem do Python do exercício anterior e a mesma pasta (`/app`) para execução da construção e do container. Na terceira linha do `Dockerfile` copiamos o arquivo `requirements.txt` que lista as dependências do projeto e na linha seguinte usamos o `pip` para fazer a instalação das dependências.

Somente após a instalação que fazemos a cópia do conteúdo da pasta `src` para dentro do container. Isto é feito pois a contrução da imagem do container é feita em camadas que podem ser reaproveitadas e, desta forma, caso seja feita alguma mundaça no código que é copiado para o container, não será necessário realizar novamente a instalação dos pacotes.

A última linha do `Dockerfile` executa o `fastapi` da mesma forma que pode ser feito pela linha de comando: `fastapi run /app/main.py --port 80`.

Este container pode ser construído usando `docker build -t cc7261:fastapi .` e executado com `docker run -p 80:80 cc7261:fastapi` que, neste caso, para permitir o acesso externo aos endpoints que estão dentro do container temos que mapear uma porta do host (80 no nosso caso) para a porta que escolhemos usar no FastAPI (também a porta 80) e por isso temos a opção `-p 80:80` no `docker run`.

Uma forma de termos a execução do serviço de forma padronizada sem correr o risco de esquecer dos parâmetros é usando o `docker compose`, como no exercício anterior.

## Docker-compose usando as duas imagens

No exercício anterior usamos o `docker-compose.yaml` para especificar um serviço que possuía 10 réplicas. Desta vez vamos executar este mesmo serviço junto com o FastAPI implementado nas seções anteriores, porém como só podemos mapear uma porta de um container a uma certa porta do host, teremos apenas um container de FastAPI mapeado a porta 80 do host, como mosta o YAML a seguir:

```yaml
services:

  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
    image: cc7261:fastapi
    container_name: fastapi
    ports:
      - 80:80
    volumes:
      - ./src:/app

  py-random:
    image: cc7261:random
    deploy:
      replicas: 10
```
A primeira linha deste `docker-compose.yaml` é a mesma que do exercício anterior e as últimas 4 linhas apresentam o uso da imagem criada no exercício anterior para a geração de 10 réplicas do mesmo container.

A terceira linha começa a especificação do container com o FastAPI e, da mesma forma que antes, faremos a construção (`build`) do container a partir do arquivo `Dockerfile` (`dockerfile`) e do contexto da pasta atual (`.`), gerando a imagem (`image`) `cc7261:fastapi`. Durante a execução, este container terá o nome (`container_name`) de `fastapi`, mapeará a porta (`ports`) 80 do container para a porta 80 do host (`-80:80`) e montará a pasta `./src` do host na pasta `/app` do container.

Após a execução do comando `docker compose up` será possível acessar os endpoints do FastAPI da mesma forma que fizemos no primeiro laboratório, além de vermos os números aleatórios sendo exibidos no terminal, como no exercício anterior.
