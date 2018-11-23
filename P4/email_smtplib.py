import sys
import smtplib
import getpass
import email.message, email.policy, email.utils


server="smtp.gmail.com"
port=587
fromaddr="nahuelcostacorteza@gmail.com"
toaddr="nahuelcostacortez@gmail.com"
subject="Prueba"
data="Mensaje de prueba"

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

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

try:  
    server = smtplib.SMTP(server, port)
    server.set_debuglevel(1)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, binario)
    server.close()

    print("Email enviado")

except :  
    print("Algo fue mal: "+sys.exc_info()[0])
    sys.exit()
