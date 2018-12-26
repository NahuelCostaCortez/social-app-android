from flask import request, abort, jsonify
from .. import db
from . import api
from ..models import Amigo
from .. import fcm
@api.route("/amigo/<int:id>")
def get_amigo(id):
    """
    Retorna JSON con información sobre el amigo cuyo id recibe como parámetro
    o un error 404 si no lo encuentra.
    """
    amigo = Amigo.query.get_or_404(id)
    amigodict = {'id': amigo.id, 'name': amigo.name,
                 'lati': amigo.lati, 'longi': amigo.longi, 'device':amigo.device}
    return jsonify(amigodict) 

@api.route("/amigo/byName/<name>") 
def get_amigo_by_name(name):
    """
    Busca el amigo por su nombre en la base de datos. Si no lo encuentra
    retorna un error 404. Si lo encuentra retorna el JSON con sus datos
    """
    amigo = Amigo.query.filter_by(name = name).first()
    if not amigo:
        abort(404, "No se encuentra ningún amigo con ese nombre")
    amigodict = {'id': amigo.id, 'name': amigo.name,
                 'lati': amigo.lati, 'longi': amigo.longi, 'device':amigo.device}
    return jsonify(amigodict)

@api.route("/amigos") 
def list_amigos():
    """
    Retorna un JSON con la lista de amigos. Cada amigo es un diccionario
    con los campos 'id', 'name', 'lati' y 'longi'
    """
    # A completar
    amigosall = []
    amigos = Amigo.query.all()
    if not amigos:
        abort(404, "No se encuentran amigos")
    for amigo in amigos:
        amigodict = {'id': amigo.id, 'name': amigo.name, 'lati': amigo.lati, 'longi': amigo.longi, 'device':amigo.device}
        amigosall.append(amigodict)
    return jsonify(amigosall); 

@api.route("/devices")
def list_devices():
    """
    Retorna un JSON con los device no nulos (ni cadenas vacías). 
    """
    # A completar
    devicesall = []
    amigos = Amigo.query.all()
    if not amigos:
        abort(404, "No se encuentran amigos")
    for amigo in amigos:
        if amigo.device != False:
            devicesall.append(amigo.device)
    return jsonify(devicesall);


@api.route("/amigo/<int:id>", methods=["PUT"]) 
def edit_amigo(id):
    """
    Modifica en la base de datos el amigo cuyo id recibe como parámetro.
    Retorna el JSON con el amigo tras la modificación
    """
    # Obtenemos el amigo a partir de su ID
    amigo = Amigo.query.get_or_404(id)
    # Comprobamos que hemos recibido JSON como parte del PUT
    if not request.json:
        abort(422, "No se ha enviado JSON")
    # Intentamos extraer campos del JSON (si no están presentes) la extracción retornará None
    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")
    device = request.json.get("device")
    # Usamos los campos que estén presentes para actualizar el objeto amigo
    if name:
        amigo.name = name
    if lati:
        amigo.lati = lati
    if longi:
        amigo.longi = longi
    if device:
        amigo.device = device
    # Finalmente, si hemos cambiado algo en el objeto amigo, hacemos el commit a la base de datos para que se guarden las modificaciones
    if name or lati or longi:
        db.session.commit()
    # Y retornamos el JSON con los nuevos datos
    amigodict = {"id": amigo.id, "name": amigo.name,
                 "longi": amigo.longi, "lati": amigo.lati, 'device':amigo.device }
    fcm.notificar_amigos("Amigo se mueve")
    return jsonify(amigodict)

@api.route("/amigo/<int:id>", methods=["DELETE"]) 
def delete_amigo(id):
    """
    Elimina un amigo cuyo id recibe como parámetro de la base de datos.
    """
    # A completar
    """
    Modifica en la base de datos el amigo cuyo id recibe como parámetro.
    Retorna el JSON con el amigo tras la modificación
    """
    # Obtenemos el amigo a partir de su ID
    amigo = Amigo.query.get_or_404(id)
    # Una vez obtenido, lo borramos
    db.session.delete(amigo)
    db.session.commit()
    #En este caso no hay nada que retornar, pero es habitual hacer que el código de estado HTTP sea 204 "No content" en lugar de 200 "OK"
    fcm.notificar_amigos("Amigo borrado")
    return ('', 204) 

@api.route("/amigos", methods=["POST"]) 
def new_amigo():
    """
    Modifica en la base de datos añadiendo un amigo cuyos datos
    recibe en JSON.
    Retorna el JSON con el amigo tras la creación, para que el cliente
    pueda conocer el id del amigo recién creado.
    """
    # Comprobamos que hemos recibido JSON como parte del PUT
    if not request.json:
        abort(422, "No se ha enviado JSON")
    # Intentamos extraer campos del JSON (si no están presentes) la extracción retornará None
    name = request.json.get("name")
    # Si no hay nombre, rechazamos la petición
    if not name:
        abort(422, "El JSON no incluye el campo 'name'")
    # Si el nombre ya existe en la base de datos, también lo rechazamos
    amigo = Amigo.query.filter_by(name = name).first()
    if amigo:
        abort(422, "Ya existe un amigo con ese nombre")
    # En caso contrario, tomamos latitud y longitud. Si no vienen les damos un valor de 0
    lati = request.json.get("lati", "0")
    longi = request.json.get("longi", "0")
    device = request.json.get("device","None")
    # Creamos un nuevo amigo con esos datos
    amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
    db.session.add(amigo)
    db.session.commit()
    # Y retornamos el JSON con los datos del nuevo amigo
    amigodict = {"id": amigo.id, "name": amigo.name,
                 "longi": amigo.longi, "lati": amigo.lati,'device':amigo.device}
    fcm.notificar_amigos("Nuevo amigo")
    return jsonify(amigodict)
