import socket
import sys
import random
import hashlib
from hashlib import md5

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puerto=9999
respuesta="OK"
lista = []
if len(sys.argv) == 2:
	puerto=int(sys.argv[1])
s.bind(("", puerto))

while True:
	datagrama, origen = s.recvfrom(1024)

	#tras recibir el datagrama decide aleatoriamente con una probabilidad del 50% si simulará no haberlo recibido
	if random.randint(0,100) > 50:
		print("Simulando paquete perdido")
	else:
		hash = hashlib.md5(datagrama)
		if hash in lista:
			s.sendto(respuesta.encode("utf8"), origen)
		else:
			lista.append(hash)
			respuesta="OK"+str(hash)
			print("Contenido del datagrama:")
			print(datagrama.decode("utf-8"))
			print("Direccion de la que proviene", origen)
			s.sendto(respuesta.encode("utf8"), origen)



