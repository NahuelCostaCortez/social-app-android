import dns.resolver

respuesta = dns.resolver.query('apple.com')
for variable in respuesta:
    print(variable)
#print(respuesta.response)
