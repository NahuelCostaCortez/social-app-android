
from flask import render_template, redirect, url_for, request, abort
from . import html
from ..models import Amigo
from flask import render_template, redirect, url_for
from .. import db

@html.route("/amigos")
def tabla_amigos():
    """
    Obtiene la lista de amigos de la base de datos y la
    devuelve en una tabla HTML.
    """
    amigos = Amigo.query.all()
    return render_template("tabla_amigos.html",
                           amigos=amigos)

@html.route("/delete_amigo/<int:id>")
def delete_amigo(id):
    """
    Borra un amigo de la base de datos
    """
    # El método get_or_404 proporcionado por SQLAlchemy
    # se ocupa de generar un error 404 si el id no está en
    # la base de datos
    amigo = Amigo.query.get_or_404(id)
    # Una vez obtenido, lo borramos
    db.session.delete(amigo)
    db.session.commit()

    # Y redireccionamos a la vista /amigos
    return redirect(url_for('html.tabla_amigos'))

@html.route("/edit_amigo/<int:id>")
def edit_amigo(id):
    """
    Presenta un formulario para obtener datos a modificar de un amigo
    """
    amigo = Amigo.query.get_or_404(id)
    # Rellenar el template con los datos de este amigo y presentar
    # el formulario al usuario
    return render_template("edit_amigo.html", amigo=amigo)

@html.route("/new_amigo/")
def new_amigo():
    """
    Presenta un formulario para obtener datos para crear nuevo amigo
    """
    # No tenemos datos de ningún amigo previo
    # Pero podemos usar el mismo template
    return render_template("edit_amigo.html", amigo=None)

# Añadir nuevos imports en la primera línea
from flask import render_template, redirect, url_for, request, abort

# ...
@html.route("/save_amigo", methods=["POST"])
def save_amigo():
    id = request.form.get("id")
    if id is None or id == "":
        # En este caso se trata de un amigo nuevo, lo creamos
        name = request.form.get("name")
        if not name:
            # Si falta el nombre, devolvemos un error HTTP 422
            abort(422)
        # Para lati y longi permitimos que estén ausentes, y en ese caso
        # les damos un valor por defecto de "0"
        lati = request.form.get("lati", "0")
        longi = request.form.get("longi", "0")
        device = request.form.get("device", "None")

        # Creamos el amigo y lo añadimos a la base de datos
        amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
        db.session.add(amigo)
        db.session.commit()
    else:
        # En este caso se trata de un amigo de la base de datos
        amigo = Amigo.query.get_or_404(int(id))
        # Modificamos los campos que vengan en el formulario
        name = request.form.get("name")
        if name:
            amigo.name = name
        lati = request.form.get("lati")
        if lati:
            amigo.lati = lati
        longi = request.form.get("longi", "0")
        if longi:
            amigo.longi = longi
        device = request.form.get("device")
        if device:
            amigo.device = device
        # Una vez modificado, lo guardamos a la base de datos
        db.session.commit()
    # Redireccionamos hacia la tabla-lista de amigos
    return redirect(url_for("html.tabla_amigos"))
