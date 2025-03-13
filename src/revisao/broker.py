import zmq

context = zmq.Context()
poller = zmq.Poller()

client_socket = context.socket(zmq.ROUTER)
client_socket.bind("tcp://*:5557")
poller.register(client_socket, zmq.POLLIN)

server_socket = context.socket(zmq.DEALER)
server_socket.bind("tcp://*:5558")
poller.register(server_socket, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    if socks.get(client_socket) == zmq.POLLIN:
        message = client_socket.recv()
        more = client_socket.getsockopt(zmq.RCVMORE)
        if more:
            server_socket.send(message, zmq.SNDMORE)
        else:
            server_socket.send(message)

    if socks.get(server_socket) == zmq.POLLIN:
        message = server_socket.recv()
        more = server_socket.getsockopt(zmq.RCVMORE)
        if more:
            client_socket.send(message, zmq.SNDMORE)
        else:
            client_socket.send(message)

