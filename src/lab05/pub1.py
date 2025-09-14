import zmq
from time import time, sleep

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:

    msgs = [
        { "topic": "hello".encode("utf-8"), "message": "hello".encode("utf-8") },
        { "topic": "time".encode("utf-8"), "message": str(time()).encode("utf-8") },
    ]
    for msg in msgs:
        print(f"Topic: {msg['topic']} - Message: {msg['message']}", flush=True)
        pub.send_multipart([msg["topic"], msg["message"]])
    sleep(1)

pub.close()
context.close()
