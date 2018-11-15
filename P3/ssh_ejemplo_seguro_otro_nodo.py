import paramiko
import getpass
import base64

client = paramiko.SSHClient() 
key = paramiko.Ed25519Key(data=base64.decodestring(b'AAAAC3NzaC1lZDI1NTE5AAAAIOSQwlItmAozlTisbFacV+BVMAmCdDMewC62cxVh/ORZ'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key) 
client.connect('10.38.32.22', username = 'alumno',password = getpass.getpass("Introduce la contraseña: ")) 
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
client.close()
