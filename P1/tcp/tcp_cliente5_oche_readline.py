import socket
import sys

def recibe_mensaje(sd):
    print("Vuelvo a recibe mensaje")
    # Se convierte el socket en un fichero
    f = sd.makefile(encoding="utf8", newline="\r\n")
    mensaje = f.readline()   # Lee bytes hasta detectar \r\n
    # El mensaje retornado es un str, y contiene \r\n al final
    return mensaje


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
while times != 3:
    print("Envio")
    times = times + 1
    s.sendall(b"ABCDE\r\n")
times = 0
while times != 3:
    times = times + 1
    mensaje = recibe_mensaje(s)
    print("Respuesta del servidor: ",mensaje[:-2])

# Cerrar el socket y terminar
s.close()
sys.exit(0)

