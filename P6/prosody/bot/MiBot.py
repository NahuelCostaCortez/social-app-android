# coding: utf-8
from sleekxmpp import ClientXMPP
import getpass
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

class MiBot(ClientXMPP):
    # Definicion del constructor
    def __init__(self, jid, clave):
        super().__init__(jid, clave)
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)
        self.add_event_handler("chatstate_composing", self.callback_para_composing)
        self.add_event_handler("chatstate_paused", self.callback_para_paused)
        self.add_event_handler("chatstate_active", self.callback_para_active)
        self.add_event_handler("chatstate_inactive", self.callback_para_inactive)

    # Registrar el callback para el evento "session_start"
    def callback_para_session_start(self, evento):
        self.send_presence()
        self.get_roster()
    # Registrar el callback para el evento "message"
    def callback_para_message(self, evento):
        print("Recibido un mensaje de tipo %s desde %s" %
                (evento["type"], evento["from"]))
        print("Que dice: %s" % evento["body"])
        msg = self.Message()
        msg["to"] = evento["from"]
        msg["type"] = "chat"
        if evento["body"][0] == '=':
             cuerpo=evento["body"]+"="+str(eval(evento["body"][1:]))
             msg["body"] = cuerpo
             msg.send()
        else:
             cuerpo=evento["body"]+"?"
             msg["body"] = cuerpo
             msg.send()

    def callback_para_composing(self, evento):
        print("%s" % evento["from"].bare + " está escribiendo")
    def callback_para_paused(self, evento):
        print("%s" % evento["from"].bare + " ha parado de escribir")
    def callback_para_active(self, evento):
        print("%s" % evento["from"].bare + " está activo")
    def callback_para_inactive(self, evento):
        print("%s" % evento["from"].bare + " está inactivo")

#Programa principal
jid = input("JID: ")
clave = getpass.getpass("Clave: ")
puerto=5222
ip="localhost"
#ip="prosody"

# Instanciar el cliente, con el jid y clave del bot
cliente = MiBot(jid, clave)
cliente.register_plugin("xep_0085")  # chatstates
# Conectar con la IP del servidor. El puerto estándar es el 5222
cliente.connect((ip, puerto))

# Iniciar el bucle de eventos
cliente.process()

# El resto es automático. Cuando llegue el momento, nuestros
# callbacks se irán ejecutando
