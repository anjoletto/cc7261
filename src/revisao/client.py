import time
import random
import json

import zmq

context = zmq.Context()
req = context.socket(zmq.REQ)
req.connect("tcp://localhost:5557")

locations = ["i", "j", "k"]

while True:
    for loc in locations:
        print(f"Location: {loc}")
        req.send_string(loc)
        data = req.recv_string()
        print(f"{data}")
        time.sleep(1)
