# Padrão Publisher-Subscriber com tópicos com ZeroMQ

Vamos aproveitar o código usado na aula para fazer algumas modificações e adicionar a parte de tópicos no padrão pub/sub.

Desta vez vamos ter 2 publishers postando em tópicos direrentes e 3 subscribers lendo de combinações de tópicos.

## Publishers com tópicos

Para fazer com que os publishers enviem uma mensagem em um tópico específico não poderemos apenas enviar a mensagem e precisamos enviar o tópico e a mensagem em bytes.

Para isso as mensagens podem ser enviadas usando o `send_multipart` com uma lista de mensagens como parâmetro. O primeiro elemento desta lista deve ser o tópico e o segundo a mensagem. Um exemplo de código baseado no exemplo da aula encontra-se a seguir
```python
topic = "tempo".encode("utf-8")
message = str(time()).encode("utf-8")
pub.send_multipart([topic, message])
```

As chamadas ao `encode` são necessários pois o `send_multipart` aceita o envio de bytes, mas não trata a conversão de strings automaticamente.

Altere o código usado na aula para implementar 2 publishers. O primeiro deve publicar a hora no tópico `hora` e a string `hello` no tópico `hello`. O segundo publisher também deve publicar o `hello`, mas sua outra mensagem deve ser um número aleatório inteiro entre 1 e 10 publicado no tópico `random`.

## Subscribers lendo de tópicos

Para que o subscriber aceite ler apenas de tópicos específicos é necessário mudar as opções do socket que ele está usando.

A linha `sub.setsockopt_string(zmq.SUBSCRIBE, "")` usada no exemplo da aula faz com que o subscriber receba as mensagens de todos os tópicos e é a string que passamos como argumento da função que precisamos mudar para escolher os tópicos. Para se inscrever em mais do que um tópico podemos chamar a mesma função várias vezes. Por exemplo:
```python
sub.setsockopt_string(zmq.SUBSCRIBE, "hello")
sub.setsockopt_string(zmq.SUBSCRIBE, "time")
sub.setsockopt_string(zmq.SUBSCRIBE, "random")
```

Para o exercício, altere o código do exemplo usado em sala para ter 3 subscribers diferentes, conforme a tabela a seguir:

| sub |  hello |  time  | random |
|-----|--------|--------|--------|
| 1   | recebe | recebe | ignora |
| 2   | recebe | ignora | recebe |
| 3   | recebe | recebe | recebe |

## Docker-compose.yaml

Desta vez temos 2 publishers e 3 subscribers diferentes e o `docker-compose.yaml` desta forma não vai funcionar pois ele consegue apenas aumentar o número de réplicas do mesmo container.

Altere o arquivo para subir cada um dos publishers e subscribers que foram desenvolvidos para o exercícios e verifique se as mensagens estão sendo trocadas da forma correta.
