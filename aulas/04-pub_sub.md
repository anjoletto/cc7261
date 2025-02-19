---
title: Publish-subscribe
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

# Publish-subscribe

https://zguide.zeromq.org/

## Exemplos de PubSub

- Robot Operating System (ROS)
- Padrão de filas no RabbitMQ
- Apache Kafka pode ser usado dessa forma
- GCP Pub/Sub

## Publish-subscribe vs Request-reply

<div class="columns">
<div>

- **Request-reply**: cliente envia mensagem (request) e servidor responde (reply)
- **Publish-subscribe**: publisher publica uma mensagem e subscriber recebe a mensagem

</div>
<div>

![](https://zguide.zeromq.org/images/fig12.png)

</div>
</div>

## Pub-sub

- A mensagem é enviada de um (publisher) para todos (subscribers)
- Voltado para escalabilidade:
    - Aplicado para grande volume de dados que pode ser enviado para várias aplicações
    - Publisher envia mensagem, subscriber lê mensagem, nenhuma outra troca de mensagens acontece (back-chatter)
- Para fica mais fácil de escalar, a mensagem do publisher é enviada para grupo de multicast e subscribers se conectam a este grupo

## Problemas do formato mais simples de pub-sub

- Publishers não sabem se subscribers estão conectados, se reconectaram ou pararam de funcionar
- Subscribers não conseguem controlar a velocidade que recebem as mensagens

> Pub-sub is like a radio broadcast; you miss everything before you join, and then how much information you get depends on the quality of your reception.

https://zguide.zeromq.org/docs/chapter5/


## Problemas para o Pub-sub ser confiável
- Conexão tardia do subscriber, perdendo mensagem
- Demora para leitura de mensagens pelo subscriber, perdendo mensagens
- Subscriber perde conexão, perdendo mensagens
- Subscribers pode travar, perdendo mensagens e os dados que possuía
- Rede pode ficar sobrecarregada e perder dados
- Rede pode ficar devagar, causando overflow na fila do publisher e possível travamento


## Código do publisher (python)

```py
import time
import zmq

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
pub.bind("tcp://*:5555")

while True:
    msg = str(time.time())
    print(f"msg: {msg}")
    pub.send_string(msg)
    time.sleep(1)
```

## Código do subscriber (python)
```py
import zmq

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "")
sub.connect("tcp://localhost:5555")

while True:
    msg = sub.recv_string()
    print(f"msg: {msg}")
```

## Com proxy entre pub e sub (publisher)
```py
import time
import zmq

ctx = zmq.Context.instance()
pub = ctx.socket(zmq.PUB)
pub.connect("tcp://localhost:5555")

while True:
    msg = str(time.time())
    print(f"msg: {msg}")
    pub.send_string(msg)
    time.sleep(1)

ctx.close()
pub.close()
```

## Com proxy entre pub e sub (subscriber)
```py
import zmq

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "")
sub.connect("tcp://localhost:5556")

while True:
    msg = sub.recv_string()
    print(f"msg: {msg}")

sub.close()
ctx.close()
```

## Com proxy entre pub e sub (proxy)
```py
import zmq

ctx = zmq.Context()

pub = ctx.socket(zmq.XPUB)
pub.bind("tcp://*:5556")

sub = ctx.socket(zmq.XSUB)
sub.bind("tcp://*:5555")

zmq.proxy(pub, sub)

pub.close()
sub.close()
ctx.close()
```
