import zmq
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

socket.send_string("+ 1 2")
mensagem = socket.recv()
print(f"1 + 2 = {mensagem}")

socket.send_string("- 1 2")
mensagem = socket.recv()
print(f"1 - 2 = {mensagem}")

socket.send_string("* 1 2")
mensagem = socket.recv()
print(f"1 * 2 = {mensagem}")

socket.send_string("/ 1 2")
mensagem = socket.recv()
print(f"1 / 2 = {mensagem}")
