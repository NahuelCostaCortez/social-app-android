import paramiko
import getpass
import base64
from stat import S_ISDIR

#Creamos la conexion
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('localhost', username = 'alumno',password = getpass.getpass("Introduce la contraseña: "))

#Abrimos el canal sftp
sftp = client.open_sftp()

#Listamos las carpetas del usuario
sftp.chdir(".")  # Cambiar a esa carpeta
listado = sftp.listdir()
print("Archivos descargados en /home/alumno/ :")
for nombre in listado:
    dir="/home/alumno/"+nombre
    if not S_ISDIR(sftp.stat(nombre).st_mode):
         ndir=nombre
         sftp.get(dir, ndir)
         print(dir + " -> " + ndir)

#Cerramos la conexion
client.close()
