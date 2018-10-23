import socket
import sys
import time

def recibe_longitud():
    # Se convierte el socket en un fichero
    #f = sd.makefile(encoding="utf8", newline="\n")
    longitud = f.readline()   # Lee bytes hasta detectar \n
    # El mensaje retornado es un str, y contiene \r\n al final
    return int(longitud),f

def recv_resto_mensaje(longitud,f):
    mensaje = f.read(longitud)
    return mensaje

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Podríamos haber omitido los parámetros, pues por defecto ‘socket()‘ en python
# crea un socket de tipo TCP

#asignamos puerto si lo recibe por linea de comandos
arg = len(sys.argv)
if arg == 2:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5) # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    f = sd.makefile(encoding="utf8", newline="\n")
    while continuar:
        # Primero recibir el mensaje del cliente
        longitud,f = recibe_longitud()

        if longitud==0: # Fin de transmision de datos por parte del cliente
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False

        mensaje = recv_resto_mensaje(longitud,f)
        # Tercero, darle la vuelta
        mensaje = mensaje[::-1]

        # Finalmente, enviarle la respuesta 
        longitud = "%d\n" % len(mensaje)
        sd.sendall(bytes(longitud + mensaje, "utf8"))
	
