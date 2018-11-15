import base64
import paramiko
client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.decodestring(b'AAAAC3NzaC1lZDI1NTE5AAAAIOSQwlItmAozlTisbFacV+BVMAmCdDMewC62cxVh/ORZ'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
print("Introduce la password:")
password = input()
client.connect('localhost', username='alumno', password=password)
print("Conectado!!")

# Abrir canal sftp
sftp = client.open_sftp()

listado = sftp.listdir()
for nombre in listado:
    print(nombre)
