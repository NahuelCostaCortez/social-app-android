import poplib
import getpass
import email

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un
    # objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    # Si estas cabeceras contienen unicode hay que decodificarlas
    # lo que es un poco enrevesado
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    # Extraemos el cuerpo (este ya vendrá correctamente decodificado)
    cuerpo = msg.get_payload()

    # Pero si es multi-part, lo anterior nos retorna una lista
    # En ese caso nos quedamos con el primer elemento, que será a su
    # vez un mensaje con su propio payload
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + parte_1

    # Finalmente imprimimos un resumen, que son las cabeceras
    # extraidas y los primeros 200 caracteres del mensaje
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo)>500:
        print("...[omitido]")
    print("-"*80)

server="pop.gmail.com"
port=995

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2);

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

pop3_mail.user(username)
pop3_mail.pass_(password)

mensaje=pop3_mail.retr(1)
bytes=[]
imprime_resumen_mensaje(b"\r\n".join(mensaje[1]))

