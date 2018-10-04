import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0.5)
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
timeout = False
while linea != "FIN":
    if timeout == False:
        num=num+1
        print("Introduce linea a enviar:")
        linea = input()
        mensaje = str(num)+linea
    s.sendto(mensaje.encode("utf8"), (ip, puerto))
    #Ya envie datagrama, espero por confirmacion
    try:
        datagrama, origen = s.recvfrom(1024)
        if datagrama.decode("utf8")=="OK":
            print("Recibida confirmación")
            timeout=False
            s.settimeout(0.5)
        else:
            print("Recibido datagrama no esperado")
    except socket.timeout:
            if s.gettimeout()==2.0:
                    print("Puede que el servidor esté caído. Inténtelo más tarde")
                    sys.exit(0)
            s.settimeout(s.gettimeout() * 2)
            print("ERROR. El datagrama de confirmación no llega")
            print("Reenviando mensaje...")
            timeout=True
    except: # Otras posibles excepciones dejamos que las maneje el usuario
            raise
if linea == "FIN":
    sys.exit(0)