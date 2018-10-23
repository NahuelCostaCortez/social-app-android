import socket
import sys
import time
import struct


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
    while continuar:
        # Primero recibir el mensaje del cliente
        mensaje = sd.recv(2)
        longitud = struct.unpack(">H", mensaje[0:2])
        longitud = longitud[0]
        print("Recibo",longitud)
        mensaje = sd.recv(longitud)
        mensaje = str(mensaje, "utf8")
        print("El mensaje es entonces", mensaje)

        if longitud==0: # Fin de transmision de datos por parte del cliente
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False
            break

        # Tercero, darle la vuelta
        mensaje = mensaje[::-1]

        # Finalmente, enviarle la respuesta 
        lonbytes = struct.pack(">H", len(bytes(mensaje, "utf8")))
        sd.sendall(lonbytes + bytes(mensaje, "utf8"))


