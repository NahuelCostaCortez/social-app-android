from app import db

class Amigo(db.Model):
    """
    Definición de la tabla 'amigos' de la base de datos
    """

    __tablename__ = "amigos"

    # Lo siguiente define las columnas de la base de datos y sus tipos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    longi = db.Column(db.String(32))
    lati = db.Column(db.String(32))

    # Podemos escribir la función siguiente para implementar cómo debe
    # mostrarse un objeto de esta clase si lo imprimes desde python
    def __repr__(self):
        return "<Amigo[{}]: {}>".format(self.id, self.name)
