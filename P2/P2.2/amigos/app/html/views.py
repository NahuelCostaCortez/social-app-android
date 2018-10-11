from flask import render_template
from . import html
from ..models import Amigo

@html.route("/amigos")
def tabla_amigos():
    """
    Obtiene la lista de amigos de la base de datos y la
    devuelve en una tabla HTML.
    """
    amigos = Amigo.query.all()
    return render_template("tabla_amigos.html",
                           amigos=amigos)
