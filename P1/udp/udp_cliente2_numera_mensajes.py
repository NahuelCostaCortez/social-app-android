import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
puerto = 9999
arg = len(sys.argv)

if arg == 2:
    ip = sys.argv[1]
if arg == 3:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])

num=0
linea = ""
while linea != "FIN":
    num=num+1
    print("Introduce linea a enviar:")
    linea = input()
    mensaje = str(num)+linea
    s.sendto(mensaje.encode("utf8"), (ip, puerto))
if linea == "FIN":
    sys.exit(0)
