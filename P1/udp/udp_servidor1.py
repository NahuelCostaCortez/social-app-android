import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puerto=9999
if len(sys.argv) == 2:
	puerto=int(sys.argv[1])
s.bind(("", puerto))
while True:
	datagrama, origen = s.recvfrom(1024) 
	print("Contenido del datagrama:")
	print(datagrama.decode("utf-8"))
	print("Direccion de la que proviene", origen)


