import sys
import socket
import ssl
import getpass
import email.message, email.policy, email.utils
import io

def RecvReply(socket):
    mensaje = socket.recv(1024).decode()
    print("S: "+mensaje)
    if not(mensaje[0:3]=="+OK"):
       print("Error")
       sys.exit()
    return mensaje[4:7]

def RecvReply2(socket):
    mensaje = socket.recv(1024).decode()
    msg=mensaje
    while("\n.\r\n" not in msg):
       mensaje = socket.recv(1024).decode()
       msg+=mensaje
    buf = io.StringIO(msg)
    while True: 
       s=buf.readline()
       if "From:" in s and "h=" not in s:
          print(s)
       if "Subject:" in s and "h=" not in s:
         print(s)
         break

server="pop.gmail.com"
port=995

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

s = socket.socket()
s.connect((server, port))
sc = ssl.wrap_socket(s)
RecvReply(sc)

mensaje = "USER "+username+"\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc)

mensaje = "PASS "+password+"\r\n"
#print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc)

mensaje = "STAT\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
numMensajes=RecvReply(sc)

print("Num mensajes:"+numMensajes+"\n")

for i in range(int(numMensajes)):
   mensaje = "RETR "+ str(i+1)+"\r\n"
   print("C: "+ mensaje)
   sc.send(mensaje.encode())
   RecvReply2(sc)
