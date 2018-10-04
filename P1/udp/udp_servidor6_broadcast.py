import socket
import sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puerto=12346
respuesta="IMPLEMENTO HOLA"
if len(sys.argv) == 2:
    puerto=int(sys.argv[1])
s.bind(("", puerto))
#Se pone el socket en modo broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
while True:
    print("vuelvo al while true")
    datagrama, origen = s.recvfrom(1024)
    #Se examina contenido del datagrama
    message = datagrama.decode("utf-8")
    print("recibo un "+message)
    if message == "BUSCANDO HOLA":
        s.sendto(respuesta.encode("utf8"), origen)
        datagrama, origen = s.recvfrom(1024)
    elif message == "HOLA":
        res = message + str(origen)
        s.sendto(res.encode("utf8"), origen)

