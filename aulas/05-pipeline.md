---
title: Pipeline e Par Exclusivo
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

# Padrões Pipeline e Par Exclusivo

https://zguide.zeromq.org/


# Parallel Pipeline

## Parallel Pipeline

<div class="columns">
<div>

- Dividir e conquistar
- Ventilator: distribui as tarefas entre workers
- Worker: faz algo de útil
- Sink: recebe o resultado dos workers
- `PUSH`: somente envia mensagens e não tem função para receber
- `PULL`: somente recebe mensagens e não consegue enviar


</div>
<div>

![](https://zguide.zeromq.org/images/fig5.png)

</div>
</div>

## Ventilator (python)
```py
import zmq
import random
import time

random.seed()

ctx = zmq.Context()

# envio de mensagens para os workers
sender = ctx.socket(zmq.PUSH)
sender.bind("tcp://*:5555")

# sincronização com o sink
sink = ctx.socket(zmq.PUSH)
sink.connect("tcp://localhost:5556")

print("Pressione alguma tecla após conectar workers")
_ = input()

sink.send(b'0') # avisa o sink que os dados serão enviados

total = 0
tasks = 100
for task in range(tasks):
    workload = random.randint(1, 100) # a tarefa é esperar o tempo de workload
    total += workload
    sender.send_string(f"{workload}")

print(f"Custo total: {total}ms")
time.sleep(1)
```

## Sink (python)

```py
import sys
import time
import zmq

ctx = zmq.Context()

# abre para conexão com worker e ventilator
receiver = ctx.socket(zmq.PULL)
receiver.bind("tcp://*:5556")

s = receiver.recv() # espera por mensagem do ventilator
t_start = time.time() # inicia contagem do tempo
tasks = 100

for task_nbr in range(tasks):
    s = receiver.recv_string()
    print(".", end="")

t_end = time.time()
print(f"\nTempo total: {(t_end-t_start):.5f}s")
```

## Worker (python)
```py
import time
import zmq

ctx = zmq.Context()

# recebe mensagem do ventilator
receiver = ctx.socket(zmq.PULL)
receiver.connect("tcp://localhost:5555")

# envia mensagem para o sink
sender = ctx.socket(zmq.PUSH)
sender.connect("tcp://localhost:5556")

while True:
    workload = receiver.recv_string()
    print(f"Tempo: {workload}ms")

    time.sleep(int(workload)*0.001) # simula a execução da tarefa

    sender.send_string(f"{workload}") # envia resultado para o sink
```

## O que acontece no pipeline
- Ventilator e sink fazem bind com worker conectando: podemos conectar quantos workers forem necessários para processar em paralelo
- Necessidade de sincronizar o início do processamento: como a conexão pode demorar, se conectarmos os workers enquanto o ventilator distribui as tarefas, workers que se comunicam antes recebem mais mensagens que os outros (primeiro worker receberá muito mais mensagem)

## O que acontece no pipeline

<div class="columns">
<div>

- Balanceamento de carga: ventilator usa socket do tipo `PUSH` para distribuir as mensagens entre os workers conectados
- Pipeline tem o mesmo problema do Request-Reply com o tempo de conexão

</div>
<div>

- Fila justa (fair-queueing): sink recebe os resultados na ordem que os workers enviam as mensagens

![](https://zguide.zeromq.org/images/fig6.png)


</div>
</div>

## Como isso seria implementado?

<div class="columns">
<div>

![](https://zguide.zeromq.org/images/fig19.png)

</div>
<div>

* Pipeline com sinal para encerrar a tarefa
* Sink possui um socket do tipo `PUB` para publicar quando a tarefa deve ser encerrada
* Worker é encerrado quando recebe a mensagem (subscribe) de final de processamento

</div>
</div>
