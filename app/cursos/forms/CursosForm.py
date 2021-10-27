from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from app.models import Curso

def get_cursos():
    return Curso.query.all()

class ProgramarCursoForm(FlaskForm):
    curso = QuerySelectField(query_factory=get_cursos, get_label='nombre')
    fecha_ini = StringField('F.Inicio', validators=[DataRequired(message="Ingresa una fecha válida")])
    fecha_fin = StringField('F.Fin', validators=[DataRequired(message="Ingresa una fecha válida")])
    submit = SubmitField('Guardar')


class VerCursoForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    curso = StringField('Curso', render_kw={'readonly': True})
    fecha_ini = StringField('F.Inicio', validators=[DataRequired(message="Ingresa una fecha válida")])
    submit = SubmitField('Guardar')