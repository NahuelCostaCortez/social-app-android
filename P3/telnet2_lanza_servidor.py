import telnetlib
import getpass
import socket
import sys

HOST = "localhost"
user = "alumno"
password = "rubenchi"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

#Imprimmimos el mensaje de introduccion
print(tn.read_until(b"$").decode('ascii'))

#Ejecutamos el comando
tn.write(b"ps -ef\n")

#Almacenamos la respuesta a ese comando 
respuesta = tn.read_until(b"$").decode('ascii')

#Comprobamos si la cadena deseada esta en la respuesta
if "udp_servidor3_con_ok.py" in respuesta:
     print("El servidor ya está en ejecución")
else:
     tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")

tn.write(b"exit\n")

tn.read_until(b"$").decode('ascii')
print(tn.read_all().decode('ascii'))










