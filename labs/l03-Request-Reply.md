# Padrão Request-Reply com ZeroMQ

Continuando com o mesmo exercício das aulas anteriores, desta vez vamos implementar o gerenciador de tarefas usando o padrão Request-Reply com ZeroMQ.

## Dockerfile e docker-compose.yml

Os `Dockerfile`s para a construção das imagens são iguais aos que foram usados na aula de teoria e estão a seguir para facilitar:

```Dockerfile
FROM python:3.13.7-alpine3.21

WORKDIR /app

RUN pip install pyzmq

COPY ./cliente.py .

CMD ["python", "cliente.py"]
```

```Dockerfile
FROM python:3.13.7-alpine3.21

WORKDIR /app

RUN pip install pyzmq

COPY ./servidor.py .

CMD ["python", "servidor.py"]
```

```Dockerfile
FROM python:3.13.7-alpine3.21

WORKDIR /app

RUN pip install pyzmq

COPY ./broker.py .

CMD ["python", "broker.py"]
```

O `docker-compose.yml` será um pouco diferente para facilitar o desenvolvimento do exercício sem a necessidade de refazer as imagens a cada alteração do código e também para permitir que o usuário interaja com o container do cliente.

```yml
services:
  broker:
    build:
      context: .
      dockerfile: Dockerfile_broker
    container_name: broker
    ports:
      - 5555:5555
      - 5556:5556

  servidor:
    build:
      context: .
      dockerfile: Dockerfile_servidor
    container_name: servidor
    volumes:
      - ./servidor.py:/app/servidor.py
    depends_on:
      - broker

  cliente:
    build:
      context: .
      dockerfile: Dockerfile_cliente
    container_name: cliente
    stdin_open: true
    tty: true
    depends_on:
      - servidor
    volumes:
      - ./servidor.py:/app/servidor.py
```

Como o código do broker continua o mesmo, a imagem dele será criada apenas uma vez e usada durante o exercícios. As imagens do servidor e cliente terão um volume montado para usar o arquivo com o código que está em desenvolvimento dentro do container (portanto não é necessário recontruir as imagens a cada alteração) e o container do cliente tem as opção `tty` e `stdin_open` que permite que o usuário conecte ao container e execute comandos usando `docker attatch cliente`.

## Broker usando a função pronta do ZeroMQ

Na aula de teoria vimos a implementação do broker, que tinha como função trocar as mensagens entre os clientes e servidores. Como esta função é muito comum de ser usada, o 0MQ já possui uma implementação do broker que pode ser usada e encontra-se no código a seguir

```py
import zmq

context = zmq.Context()

client_socket = context.socket(zmq.ROUTER)
client_socket.bind("tcp://*:5555")

server_socket = context.socket(zmq.DEALER)
server_socket.bind("tcp://*:5556")

zmq.proxy(client_socket, server_socket)

client_socket.close()
server_socket.close()
context.term()
```

## Cliente e servidor

O exercício desta semana é desenvolver o gerenciador de tarefas usando Request-Reply, da mesma forma que nas semanas anteriores. Os códigos a seguir apresentam o início desta implementação, com a configuração do cliente e servidor para a conexão com o broker e a implementação da função de adicionar tarefas.

```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tarefas = dict()
cont = 0

while True:
    request = socket.recv_json()
    opcao = request["opcao"]
    dados = request["dados"]
    reply = "ERRO: função não escolhida"

    match opcao:
        case "adicionar":
            tarefas[cont] = dados
            cont += 1
            reply = "OK"
        case "atualizar":
            pass
        case "deletar":
            pass
        case "listar":
            pass
        case "buscar":
            pass
        case _ :
            reply = "ERRO: função não encontrada"

    socket.send_string(reply)
```

```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

opcao = input("Entre com a opção: ")
while opcao != "sair":
    match opcao:
        case "adicionar":
            titulo = input("Entre com a tarefa: ")
            descricao = input("Entre com a descrição da tarefa: ")

            request = {
                "opcao": "adicionar",
                "dados": {
                    "titulo": titulo,
                    "desc": descricao
                }
            }

            socket.send_json(request)
            reply = socket.recv_string()
            if reply.split(":")[0] == "ERRO":
                print(reply, flush=True)

        case "atualizar":
            pass
        case "deletar":
            pass
        case "listar":
            pass
        case "buscar":
            pass
        case _:
            print("Opção não encontrada")

    opcao = input("Entre com a opção: ")
```

O exercício desta atividade é completar o código fornecido de forma que o usuário consiga utilizar o programa da mesma forma que nas aulas anteriores. Ao final, ele deve conseguir adicionar, atualizar e remover tarefas, além de ver todas as tarefas que estão cadastradas.
