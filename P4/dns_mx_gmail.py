import dns.resolver

respuesta = dns.resolver.query("*@gmail.com", "MX")
for variable in respuesta:
    print(variable)
#print(respuesta.response)
