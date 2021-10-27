from flask import Blueprint
cursos_bp = Blueprint('cursos', __name__, template_folder='templates')
from . import routes