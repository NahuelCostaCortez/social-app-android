import socket
import sys
import struct

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
mensaje = "ABCDE"
while times != 3:
    times = times + 1
    lonbytes = struct.pack(">H", len(bytes(mensaje, "utf8")))
    s.sendall(lonbytes+bytes(mensaje, "utf8"))
    print("Envio: "+mensaje)
times = 0
while times != 3:
    times = times + 1
    mensaje = s.recv(2)
    longitud = struct.unpack(">H", mensaje[0:2])
    longitud = longitud[0]
    #mensaje = mensaje[2:2 + longitud]
    mensaje = s.recv(longitud)
    mensaje = str(mensaje, "utf8")
    print("Respuesta del servidor: ",mensaje)

# Indicar fin de mensajes. Cerrar el socket y terminar
mensaje = ""
lonbytes = struct.pack(">H", len(bytes(mensaje, "utf8")))
s.sendall(lonbytes+bytes(mensaje, "utf8"))
s.close()
sys.exit(0)

