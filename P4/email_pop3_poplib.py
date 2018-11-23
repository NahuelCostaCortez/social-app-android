import poplib
import getpass

server="pop.gmail.com"
port=995

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2);

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

pop3_mail.user(username)
pop3_mail.pass_(password)

print("Primer mensaje"+str(pop3_mail.retr(1)))

