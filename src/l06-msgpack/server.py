import zmq
import msgpack

ctx = zmq.Context()

server = ctx.socket(zmq.REP)
server.bind("tcp://*:5555")
count = 0

while True:
    msg_p = server.recv()
    msg = msgpack.unpackb(msg_p)
    count += 1
    print(f"Mensagem {count} : {msg}")

    ans = {"status": "ok", "reply": "World"}
    ans_p = msgpack.packb(ans)
    server.send(ans_p)

server.close()
ctx.close()
