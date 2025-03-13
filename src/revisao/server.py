import json
from collections import deque

import zmq

ctx = zmq.Context()
poller = zmq.Poller()

sub = ctx.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "")
sub.connect("tcp://localhost:5556")
poller.register(sub, zmq.POLLIN)


rep = ctx.socket(zmq.REP)
rep.connect("tcp://localhost:5558")
poller.register(rep, zmq.POLLIN)


data = {"i": deque(), "j": deque(), "k": deque()}

while True:
    sockets = dict(poller.poll())

    if(sockets.get(sub) == zmq.POLLIN):
        msg = sub.recv_string()
        topic, msg = msg.split(" ", 1)
        print(f"Data from {topic}")
        data[topic].append(json.loads(msg))
        if(len(data[topic]) > 5):
            data[topic].popleft()


    if(sockets.get(rep) == zmq.POLLIN):
        loc = rep.recv_string()
        print(f"Request for {loc}")
        loc_data = data.get(loc, {})
        means = dict()
        if loc_data:
            means = {key: 0 for key in loc_data[0]}
            for d in loc_data:
                for key in means:
                    means[key] += d[key]

            for key in means:
                means[key] /= len(loc_data)

        rep.send_string(json.dumps(means))


sub.close()
ctx.close()
