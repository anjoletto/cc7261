import zmq

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "j")
sub.connect("tcp://localhost:5556")

while True:
    msg = sub.recv_string()
    print(f"msg: {msg}")

sub.close()
ctx.close()
