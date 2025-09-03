import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tarefas = dict()
cont = 0

while True:
    request = socket.recv_json()
    opcao = request["opcao"]
    dados = request["dados"]
    reply = "ERRO: função não escolhida"

    match opcao:
        case "adicionar":
            tarefas[cont] = dados
            cont += 1
            reply = "OK"
        case "atualizar":
            pass
        case "deletar":
            pass
        case "listar":
            pass
        case "buscar":
            pass
        case _ :
            reply = "ERRO: função não encontrada"

    socket.send_string(reply)
