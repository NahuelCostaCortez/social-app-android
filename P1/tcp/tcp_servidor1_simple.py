import socket
import sys

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
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = sd.recv(5) # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii") # Pasar los bytes a caracteres
        # En este ejemplo se asume que el texto recibido es ascii puro
        if datos=="": # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)

