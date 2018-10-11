# La instrucción FROM indica en qué imagen nos basamos
FROM python:3.7
# Si vamos a publicar esta imagen porque pueda ser útil a otros 
# convendría dar una dirección de contacto con MAINTAINER MANTAINER Jose 
# Luis Diaz <jldiaz@uniovi.es> 

#La orden RUN ejecuta los comandos 
# siguientes dentro de un contenedor (que se crea a partir de la imagen 
# FROM), y se usan para modificar el sistema de archivos del contenedor, 
# crear carpetas, instalar paquetes, etc. Cada línea RUN es una capa 
# nueva para el sistema de archivos docker por lo que a veces se agrupan 
# comandos en un solo RUN para no crear muchas capas intermedias
RUN pip install flask && pip install gunicorn
# Observa que lo anterior usa el comando pip que esté presente en la 
# imagen python:3.7. La instalación es global, no se usan aquí entornos 
# virtuales. Pero es global dentro del contenedor, no afecta al 
# anfitrión

# Lo siguiente "instala" nuestra aplicación dentro del 
# contenedor
RUN mkdir /app 
COPY hola_flask.py /app

# WORKDIR permite especificar en qué carpeta se hallará el contenedor 
# cuando arranque
WORKDIR /app

# EXPOSE permite especificar qué puertos del contenedor serán accesibles 
# desde el anfitrión o desde otros contenedores en la misma red virtual
EXPOSE 5000

# Finalmente CMD sirve para especificar qué proceso será ejecutado 
# cuando arranque el contenedor con esta imagen
CMD ["/usr/local/bin/gunicorn", "-b",  "0.0.0.0:5000", "-w", "4", "hola_flask:app"]
