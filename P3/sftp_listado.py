import paramiko
import getpass
import base64

#Creamos la conexion
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('localhost', username = 'alumno',password = getpass.getpass("Introduce la contraseña: "))

#Abrimos el canal sftp
sftp = client.open_sftp()

#Listamos las carpetas del usuario
sftp.chdir(".")  # Cambiar a esa carpeta
listado = sftp.listdir()
print("Carpetas en /home/alumno/ :")
for nombre in listado:
    print(nombre)

#Cerramos la conexion
client.close()
