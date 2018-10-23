import socket
import sys
import time

def recibe_mensaje(sd):
    buffer = []
    seguir = True
    while seguir:
        buffer.append(sd.recv(1))
	# Si se detecta fin de linea es que el cliente ha cerrado el socket
        if(buffer[-1]==b''):
            seguir = False
	# Si se detecta un \r hay que comprobar si el siguiente byte es \n
        while buffer[-1] == b'\r':
            buffer.append(sd.recv(1))
            if(buffer[-1] == b'\n'):
                seguir = False
    return  b"".join(buffer)

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
        mensaje = recibe_mensaje(sd)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        mensaje = str(mensaje, "utf8")  # Convertir los bytes a caracteres

        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]  # slice desde el principio hasta el final -2
        print("recibido: ",linea)

        # Tercero, darle la vuelta
        linea = linea[::-1]

        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(linea + "\r\n", "utf8"))

        if linea=="": # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False

