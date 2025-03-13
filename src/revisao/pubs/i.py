import time
import random
import json
import zmq

ctx = zmq.Context.instance()
pub = ctx.socket(zmq.PUB)
pub.connect("tcp://localhost:5555")
topic = "i"

random.seed()

while True:
    data = {
        "timestamp": time.time(),
        "temperatura": random.randint(20, 33),
        "humidade": random.randint(40, 70),
        "chuva": random.randint(0, 1)
    }

    msg = f"{topic} {json.dumps(data)}"
    print(msg)
    pub.send_string(msg)
    #time.sleep(1)

ctx.close()
pub.close()
