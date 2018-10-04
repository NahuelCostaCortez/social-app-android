import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mensaje_inicial = "BUSCANDO HOLA"
mensaje = "HOLA"
puerto = 12346
arg = len(sys.argv)
if arg == 2:
    ip = sys.argv[1]
#variable para controlar quien es el primer servidor que respondee
servidor = False
#Se pone el socket en modo broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(mensaje_inicial.encode("utf8"), (ip,puerto))
#mensaje = "HOLA"
#s.sendto(mensaje.encode("utf8"), ('192.168.0.164', 12346))

while True:
    try:
        #Espera por posibles respuestas de servidores
        s.settimeout(2.0)
        datagrama, origen = s.recvfrom(1024)
        print(datagrama.decode("utf8")+" desde",origen)
        if servidor == False:
            servidor = origen
    except socket.timeout:
        #Se asume que no hay mas servidores
        s.sendto(mensaje.encode("utf8"), servidor)
        break
    except: # Otras posibles excepciones
        raise
if servidor!=False:
    s.sendto(mensaje.encode("utf8"), servidor)
    s.connect(servidor)
    respuesta = s.recv(1024)
    print("Respuesta del servidor: "+respuesta.decode("utf8"))
else:
    print("No hay ningún servidor disponible")

sys.exit(0)
