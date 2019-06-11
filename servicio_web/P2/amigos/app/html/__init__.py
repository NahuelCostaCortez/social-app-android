from flask import Blueprint

html = Blueprint('html', __name__)

from . import views
