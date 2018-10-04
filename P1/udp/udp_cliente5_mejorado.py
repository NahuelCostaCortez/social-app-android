import socket
import sys
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
puerto = 9999
arg = len(sys.argv)

if arg == 2:
    ip = sys.argv[1]
if arg == 3:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])


linea = ""
timeout = False

while linea != "FIN":
    if timeout == False:
        print("Introduce linea a enviar:")
        linea=input()
    s.sendto(linea.encode("utf8"), (ip, puerto))
    hash = hashlib.md5(bytes(linea, "utf"))
    s.settimeout(0.1)
    try:
        s.connect((ip, puerto))
        datagrama = s.recv(1024) # Tamaño máximo a recibir
        datagrama = datagrama.decode("utf8")
        print("Recibido",datagrama[0:2])
        if datagrama[0:2]=="OK":
            print("Recibida confirmación del datagrama con ID", datagrama[2:])
            timeout = False
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

