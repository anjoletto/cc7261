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

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

i = 0
while True:
    print(f"Mensagem {i}:", end=" ")
    socket.send(b"Hello")
    mensagem = socket.recv()
    print(f"{mensagem}")
    i += 1

```

## Execução

```sh
python servidor.py
```

Em outro terminal
```sh
python cliente.py
```

* e se inverter a ordem?
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

## Código do cliente (python)


```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555") # conecta no broker local

msg_count = 0
while True:
    print(f"Mensagem {msg_count}:", end=" ")
    socket.send(b"Hello") # envia mensagem (request)
    mensagem = socket.recv() # recebe mensagem (reply)
    print(f"{mensagem}")
    msg_count += 1
```

## Código do servidor (python)


```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5556") # conecta no broker local
msg_count = 0

while True:
    print(f"Mensagem {msg_count}:", end=" ")
    message = socket.recv()
    socket.send_string("World")
    print(f"{message}")
    msg_count += 1
```

## Código do broker (python) - parte 1

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

## Código do broker (python) - parte 2

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
