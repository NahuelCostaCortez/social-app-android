import email.message, email.policy, email.utils

server=relay.uniovi.es
port=25
fromaddr=uo251652@uniovi.es
toaddr=nahuxperia@gmail.com
subject=Prueba
data=Mensaje de prueba

mensaje = email.message.EmailMessage()
mensaje['To'] = addr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))
binario+=(b("\r\n.\r\n)")

s = socket.socket()
s.connect((gethostbyname(server),port))

s.send(binario)
#mensaje = s.recv(80)



'''
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
'''
