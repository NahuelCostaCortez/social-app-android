import paramiko
client = paramiko.SSHClient()
client.connect('localhost', username='alumno', password='clave-mal')
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
client.close()
