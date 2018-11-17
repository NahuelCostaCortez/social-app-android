import dns.resolver

respuesta = dns.resolver.query('en.wikipedia.org')
print("IP: "+str(respuesta[0].address))
print("Respuesta completa: "+str(respuesta.response))
