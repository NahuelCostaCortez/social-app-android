import socket
import sys
import random 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puerto=9999
if len(sys.argv) == 2:
	puerto=int(sys.argv[1])
s.bind(("", puerto))
while True:
	datagrama, origen = s.recvfrom(1024) # 1024 es el máximo tamaño esperado
	#tras recibir el datagrama decide aleatoriamente con una probabilidad del 50% si simulará no haberlo recibido
	if random.randint(0,100) > 50:
		print("Simulando paquete perdido")
	else:
		print("Contenido del datagrama:")
		print(datagrama.decode("utf-8"))
		print("Direccion de la que proviene", origen)


