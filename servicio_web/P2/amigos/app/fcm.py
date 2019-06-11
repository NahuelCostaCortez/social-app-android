from pyfcm import FCMNotification
from .models import Amigo

def notificar_amigos(body):
   registration_ids = []
   push_service = FCMNotification(
                        api_key="AIzaSyDVYHX5NI7vU632yjKtvlTrsUEjaLPEWwc")
   amigos = Amigo.query.all()
   for amigo in amigos:
      if amigo.device != False:
         registration_ids.append(amigo.device)   
   message_title = "Amigos"
   message_body = body
   result = push_service.notify_multiple_devices(
                        registration_ids=registration_ids,
                        message_title=message_title,
                        message_body=message_body)

#notificar_amigos("hola")
