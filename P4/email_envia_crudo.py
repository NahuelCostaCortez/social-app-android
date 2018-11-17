import sys
import socket 

def RecvReply(socket, codigo):
    mensaje = socket.recv(1024).decode()
    print("S: "+mensaje)
    if not(int(mensaje[0:3])==codigo):
       print("Error")
       sys.exit()

server="relay.uniovi.es"
port=25
fromaddr="uo251652@uniovi.es"
toaddr="uo251652@uniovi.es"
subject="Prueba"
data="Mensaje de prueba"

s = socket.socket()
ipservidor=socket.gethostbyname(server)
s.connect((ipservidor,port))
print("Conectado a servidor: "+ipservidor) 
mensaje = s.recv(1024).decode()
print("S: "+mensaje)

mensaje = "HELO "+server+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,250)

mensaje="MAIL FROM: "+fromaddr+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,250)

mensaje="RCPT TO: "+toaddr+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,250)

mensaje= "DATA"+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,354)

message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)
s.send(message.encode())
RecvReply(s,250)

mensaje="QUIT"+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,221)



