import socket
import sys

def recibe_longitud(sd):
    # Se convierte el socket en un fichero
    f = sd.makefile(encoding="utf8", newline="\n")
    longitud = f.readline()   # Lee bytes hasta detectar \n
    # El mensaje retornado es un str, y contiene \r\n al final
    return int(longitud),f

def recv_resto_mensaje(longitud,f):
    mensaje = f.read(longitud)
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
mensaje = "ABCDE"
while times != 3:
    times = times + 1
    longitud  = "%d\n" % len(bytes(mensaje, "utf8"))
    print("voy a enviar: ", (bytes(longitud + mensaje, "utf8")))
    s.sendall(bytes(longitud + mensaje, "utf8"))
times = 0
while times != 3:
    times = times + 1
    longitud,f = recibe_longitud(s)
    mensaje = recv_resto_mensaje(longitud,f)
    print("Respuesta del servidor: ",mensaje)

# Indicar fin de mensajes. Cerrar el socket y terminar
mensaje = ""
longitud  = "%d\n" % len(bytes(mensaje, "utf8"))
s.sendall(bytes(longitud + mensaje, "utf8"))
s.close()
sys.exit(0)

