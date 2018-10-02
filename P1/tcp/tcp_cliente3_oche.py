import socket
import sys

# Creacion de un socket TCP
s = socket.socket()

ip = "localhost"
puerto = 9999
arg = len(sys.argv)

if arg == 2:
    ip = sys.argv[1]
if arg == 3:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])

# Se conecta al servidor
s.connect((ip,puerto))

times = 0
while times != 2:
    times = times + 1
    s.sendall(b"ABCDE\r\n")
    mensaje = s.recv(80)
    print("Respuesta del servidor: ",str(mensaje, "utf8"))

# Ultimo envio cerrar el socket y terminar
s.sendall(b"FINAL\r\n")
mensaje = s.recv(80)
print("Respuesta del servidor: ",str(mensaje, "utf8"))
s.close()
sys.exit(0)

