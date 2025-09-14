import zmq
from time import sleep
from random import randint

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:

    msgs = [
        { "topic": "hello".encode("utf-8"), "message": "hello".encode("utf-8") },
        { "topic": "random".encode("utf-8"), "message": str(randint(1,10)).encode("utf-8") },
    ]
    for msg in msgs:
        print(f"Topic: {msg['topic']} - Message: {msg['message']}", flush=True)
        pub.send_multipart([msg["topic"], msg["topic"]])
    sleep(1)

pub.close()
context.close()
