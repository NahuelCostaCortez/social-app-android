import socket

parametros=socket.getaddrinfo("en.wikipedia.org", "www")
param=parametros[0]
s = socket.socket(param[0], param[1], param[2]) 
print("Creado socket con parametros: "+ str(param[0])+ " " + str(param[1]) + " " + str(param[2]))
ip = param[4][0]
puerto = param[4][1]
print("Creada conexion a IP: "+ ip + " y puerto: "+ str(puerto))
s.connect((ip,puerto))
s.sendall(b"GET / HTTP/1.1\r\n\r\n")
mensaje = s.recv(1024)
print("Respuesta del servidor: ",str(mensaje, "utf8"))
