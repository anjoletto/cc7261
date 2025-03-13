import zmq
import msgpack

ctx = zmq.Context()

client = ctx.socket(zmq.REQ)
client.connect("tcp://localhost:5555")
count = 0

while True:
    count += 1
    msg = {"request": "Hello", "count": count}
    msg_p = msgpack.packb(msg)
    client.send(msg_p)

    reply_p = client.recv()
    reply = msgpack.unpackb(reply_p)
    print(f"Received reply: {reply}")
