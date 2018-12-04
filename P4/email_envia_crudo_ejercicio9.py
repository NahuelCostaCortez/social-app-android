import sys
import socket 
import email.message, email.policy, email.utils

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

mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba")
with open("logoatc.gif", "rb") as f:
    gif = f.read()
mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")
binario = mensaje.as_bytes()
binario+=bytes('\r\n.\r\n', 'utf-8')
print(binario.decode("utf-8"))
s.send(binario)
RecvReply(s,250)

mensaje="QUIT"+"\r\n"
print("C: "+ mensaje)
s.send(mensaje.encode())
RecvReply(s,221)

