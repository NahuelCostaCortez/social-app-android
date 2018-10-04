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
while times != 4:
    times = times + 1
    s.send(b"ABCDE")

# Ultimo envio cerrar el socket y terminar
s.send(b"FINAL")
s.close()
sys.exit(0)

