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
resp = f.retrlines("MLSD", acumular)
for l in lista:
    if("type=file" in l):
       lseparado=l.split(";")
       var = lseparado[7].strip()
       print(var)
       # Enviamos comando LIST e indicamos el callback para tratar la respuesta
       f_local = open(var, "wb") # Creamos el fichero local
                                         # importante abrirlo en modo binario "$
       result = f.retrbinary("RETR "+var,    # Enviar peticion de fichero
            f_local.write) 
       f_local.close()
       print(result)
       
