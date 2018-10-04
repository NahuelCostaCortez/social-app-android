import socket
import sys

def recibe_mensaje(sd):
    buffer = []
    seguir = True
    while seguir:
        buffer.append(sd.recv(1))
        if(buffer[-1]==b''):
            seguir = False
        while buffer[-1] == b'\r':
            buffer.append(sd.recv(1))
            if(buffer[-1] == b'\n'):
                seguir = False
    return  b"".join(buffer)

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
    times = times + 1
    s.sendall(b"ABCDE\r\n")
times = 0
while times != 3:
    times = times + 1
    mensaje = recibe_mensaje(s)
    print("Respuesta del servidor: ",repr(str(mensaje[:-2], "utf8")))

# Cerrar el socket y terminar
s.close()
sys.exit(0)

