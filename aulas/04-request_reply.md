---
title: Request-Reply
author: Leonardo Anjoletto Ferreira
theme: custom
paginate: true
lang: pt-br
---
<!-- headingDivider: 2 -->

<!--
_header: CC7261 - Sistemas Distribuídos
_footer: Leonardo Anjoletto Ferreira
_paginate: skip
-->

# Request-Reply

https://zguide.zeromq.org/

## Antes de mais nada

* Não vamos usar sockets
* Mas vamos usar sockets:
    - Nível mais baixo do que vimos antes
    - Mas não tão baixo quanto em S.O.

## Advanced Message Queuing Protocol (AMQP)
- Projeto inicial em 2003
- Protocolo para troca de mensagens
- Possui algumas implementações: Apache Qpid, RabbitMQ, Apache ActiveMQ, IBM MQ

## ZeroMQ

- Mais simples que o AMQP
- Permite a construção de diversos padrões (esta e próximas aulas)
- Podemos escolher entre 28 linguagens
- Curiosidade: usado pelo CERN para a troca de informações entre os aceleradores de partículas
* Vamos fazer (quase tudo) na mão desta vez

## Padrões de troca de mensagem
- Request-reply: cliente envia mensagem (request) e servidor responde (reply)
- Publish-subscribe: servidor publica (publish) e clientes se inscrevem (subscribe) para receber as mensagem
- Pipeline: cliente envia mensagem, workers trabalham em paralelo na mensagem, um cliente recebe o resultado (dividir e conquistar)

## Request-reply (com 0MQ)

<div class="columns">
<div>

![h:500px](https://zguide.zeromq.org/images/fig2.png)

</div>
<div>

- conexão via socket entre os processos
- servidor abre uma conexão do tipo `zmq.REP`
- cliente se conecta usando `zmq.REQ`
- cliente e servidor trocam mensagem em bytes
* **cliente inicia enviando mensagem para o servidor**

</div>
</div>

## Docker (para facilitar algumas coisas)

- O `docker-compose.yaml`:
    - mesmo formato que usamos com gRPC
    - somente alteramos a porta do servidor para 5555
- Dokerfile do cliente e servidor:
    - removemos a parte do gRPC (instalação, cópia do arquivo `proto` e  compilação)
    - instalamos o `pyzmq` pelo `pip`

## Dockerfile
```yaml
services:
  servidor:
    build:
      context: .
      dockerfile: Dockerfile_servidor
    container_name: servidor
    ports:
      - 5555:5555
  cliente:
    build:
      context: .
      dockerfile: Dockerfile_cliente
    container_name: cliente
    depends_on:
      - servidor
```

## Dockerfile

<div class="columns">
<div>

### servidor

```docker
FROM python:3.13.7-alpine3.21
WORKDIR /app
RUN pip install pyzmq
COPY ./servidor.py .
CMD ["python", "servidor.py"]
```
</div>
<div>

### cliente

```docker
FROM python:3.13.7-alpine3.21
WORKDIR /app
RUN pip install pyzmq
COPY ./cliente.py .
CMD ["python", "cliente.py"]
```

</div>
</div>

## Código para o servidor (Python)
```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Mensagem recebida: {message}")
    socket.send_string("World")
```

## Código para o cliente (Python)
```py
import zmq
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://servidor:5555")

i = 0
while True:
    print(f"Mensagem {i}:", end=" ", flush=True)
    socket.send(b"Hello")
    mensagem = socket.recv()
    print(f"{mensagem}")
    i += 1
    sleep(0.5)
```

## Execução

```sh
docker compose up
```

* e se inverter a ordem? (trocar o `depends_on` do `docker-compose.yml`)
* e ser o servidor cair e voltar?
* o que é o `b` antes da string?

## Outras combinações de conexão

<div class="columns">
<div>

- Request - Reply
- Dealer - Reply
- Request - Router
- Dealer - Router
- Dealer - Dealer
- Router - Router

* Dealer: tipo request, mas assíncrono
* Router: tipo reply, mas assíncrono

</div>
<div>

Padrão de balanceamento de carga

![](https://zguide.zeromq.org/images/fig32.png)

</div>
</div>

## Código do broker - parte 1/2

```py
import zmq

context = zmq.Context()
poller = zmq.Poller()

client_socket = context.socket(zmq.ROUTER)
client_socket.bind("tcp://*:5555")
poller.register(client_socket, zmq.POLLIN)
client_count = 0

server_socket = context.socket(zmq.DEALER)
server_socket.bind("tcp://*:5556")
poller.register(server_socket, zmq.POLLIN)
server_count = 0
```

## Código do broker - parte 2/2

```py
while True:
    socks = dict(poller.poll())

    if socks.get(client_socket) == zmq.POLLIN:
        client_count += 1
        message = client_socket.recv()
        more = client_socket.getsockopt(zmq.RCVMORE)
        if more:
            server_socket.send(message, zmq.SNDMORE)
        else:
            server_socket.send(message)
        print(f"Client messages: {client_count}")

    if socks.get(server_socket) == zmq.POLLIN:
        server_count += 1
        message = server_socket.recv()
        more = server_socket.getsockopt(zmq.RCVMORE)
        if more:
            client_socket.send(message, zmq.SNDMORE)
        else:
            client_socket.send(message)
        print(f"Server messages: {server_count}")

```

## Código do cliente (python)


```py
import zmq
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

i = 0
while True:
    print(f"Mensagem {i}:", end=" ", flush=True)
    socket.send(b"Hello")
    mensagem = socket.recv()
    print(f"{mensagem}", flush=True)
    i += 1
    sleep(0.5)
```

## Código do servidor (python)


```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

while True:
    message = socket.recv()
    print(f"Mensagem recebida: {message}", flush=True)
    socket.send_string("World")

```

## Dockerfiles

<div class="columns">
<div>

```docker
FROM python:3.13.7-alpine3.21
WORKDIR /app
RUN pip install pyzmq
COPY ./broker.py .
CMD ["python", "broker.py"]
```

```docker
FROM python:3.13.7-alpine3.21
WORKDIR /app
RUN pip install pyzmq
COPY ./servidor.py .
CMD ["python", "servidor.py"]
```

</div>
<div>

```docker
FROM python:3.13.7-alpine3.21
WORKDIR /app
RUN pip install pyzmq
COPY ./cliente.py .
CMD ["python", "cliente.py"]
```

</div>
</div>

## docker-compose.yml - parte 1/2

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
```
## docker-compose.yml - parte 2/2

```yml
  servidor:
    build:
      context: .
      dockerfile: Dockerfile_servidor
    depends_on:
      - broker

  cliente:
    build:
      context: .
      dockerfile: Dockerfile_cliente
    depends_on:
      - servidor
```
