import paramiko
import getpass
import base64

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.decodestring(b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCvxyQ4eeYE9imD4VDghUw6nsMOoFRTLeNkuxXYOuOC6IjiADLzGMpUOAVhNwTBUYXrsi/bsPUnOBKhPSgtg0S+nRVEyaBRXcLp+5Qug78hce21fA6aBE6o7s+NfKQCqHsJhvi3DIVSPyVlfWHB7FSdzs4azrs4kwRl7PIGLMXQD+G1om2/6JPqgqzNwo4RvrS9w61Bqx6SAjTV3HU4KB6L2qMRlMqBH/ULJrRmr4FXtrFxiKaq6ffHBB79GrO5AkDSgHW1LApkpqJANQO17N+73sPmemGI41L0dvmqFtGa2gX0BPb//84lOJUIyVbWiYCZa1uK6vU9iZCPRhbjwA1V'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
client.connect('localhost', username = 'alumno',password = getpass.getpass("Introduce la contraseña: "))
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
client.close()
