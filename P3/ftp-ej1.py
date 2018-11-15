# Comenzamos por definir el callback, que es una funcion
# que sera llamada por cada linea recibida del servidor
# Este callback se limita a acumular las lineas en una
# variable global llamada lista

lista = []

def acumular(linea):
    lista.append(linea)

import ftplib, getpass

clave = getpass.getpass("Clave:")

f = ftplib.FTP("localhost")  # Conecta al servidor
f.login("alumno", clave)   # Envia comandos USER y PASS
f.cwd("/home/alumno")             # Envia comando CWD

# Borramos la lista donde recibiremos la respuesta
lista = []
# Enviamos comando LIST e indicamos el callback para tratar la respuesta
resp = f.retrlines("LIST", acumular)

# Mostramos los resultados
print("Respuesta del protocolo: ", resp)
print("Contenidos de la carpeta remota:")
for l in lista:
    print(l)
