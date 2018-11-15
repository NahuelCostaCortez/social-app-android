# Comenzamos por definir el callback, que es una funcion
# que sera llamada por cada linea recibida del servidor
# Este callback se limita a acumular las lineas en una
# variable global llamada lista

lista = []

def acumular(linea):
    lista.append(linea)

import ftplib, getpass

clave = getpass.getpass("Contraseña: ")

f = ftplib.FTP("localhost")  # Conecta al servidor
f.login("alumno", clave)   # Envia comandos USER y PASS
f.cwd("/home/alumno")             # Envia comando CWD

# Borramos la lista donde recibiremos la respuesta
lista = []
# Enviamos comando LIST e indicamos el callback para tratar la respuesta
f_local = open("prueba-copia.txt", "wb") # Creamos el fichero local
                                         # importante abrirlo en modo binario "b"
result = f.retrbinary("RETR prueba.py",    # Enviar peticion de fichero
            f_local.write)      # Funcion a ejecutar por cada bloque recibido
f_local.close()
print(result)
