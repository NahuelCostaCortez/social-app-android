import sys
import socket
import ssl
import base64
import getpass
import email.message, email.policy, email.utils

def RecvReply(socket, codigo):
    mensaje = socket.recv(1024).decode()
    print("S: "+mensaje)
    if not(int(mensaje[0:3])==codigo):
       print("Error")
       sys.exit()

server="smtp.gmail.com"
port=587
#fromaddr="nahuelcostacortez@gmail.com"
fromaddr="anonimo@example.com"
toaddr="uo251652@uniovi.es"
subject="Prueba"
data="Mensaje de prueba"

s = socket.socket()
ipservidor=socket.gethostbyname(server)
s.connect((ipservidor,port))
print("Conectado a servidor: "+ipservidor) 
mensaje = s.recv(1024).decode()
print("S: "+mensaje)

mensaje = "EHLO "+server+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,250)

mensaje = "starttls \r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,220)

sc = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)

mensaje = "auth login \r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc,334)

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

sc.send(base64.b64encode(username.encode("ascii"))+b'\r\n')
# Leer respuesta (esperamos 334)
RecvReply(sc,334)

sc.send(base64.b64encode(password.encode("utf8"))+b'\r\n')
# Leer respuesta (esperamos 235)
RecvReply(sc,235)

mensaje="MAIL FROM: <"+fromaddr+">\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc,250)

mensaje="RCPT TO: <"+toaddr+">\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc,250)

mensaje= "DATA"+"\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc,354)

mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba")
#with open("logoatc.gif", "rb") as f:
#    gif = f.read()
#mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")
binario = mensaje.as_bytes()
binario+=bytes('\r\n.\r\n', 'utf-8')
print(binario.decode("utf-8"))
sc.send(binario)
RecvReply(sc,250)

mensaje="QUIT"+"\r\n"
print("C: "+ mensaje)
sc.send(mensaje.encode())
RecvReply(sc,221)
