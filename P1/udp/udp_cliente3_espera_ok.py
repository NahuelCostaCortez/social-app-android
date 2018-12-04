import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2.0)
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
    mensaje = str(num)+": "+linea
    s.sendto(mensaje.encode("utf8"), (ip, puerto))
    #Ya envie datagrama, espero por confirmacion
    try:
        datagrama, origen = s.recvfrom(1024)
        if datagrama.decode("utf8")=="OK":
            print("Recibida confirmación")
        else:
            print("Recibido datagrama no esperado")
    except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")
    except: # Otras posibles excepciones dejamos que las maneje el usuario
            raise
if linea == "FIN":
    sys.exit(0)
