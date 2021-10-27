from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class VerAlumnoForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    nombre = StringField('Nombre')
    apellido = StringField('Apellido')
    dni = StringField('DNI')
    correo = StringField('Correo')
    celular = StringField('Celular')
    slug = StringField('Slug')
    submit = SubmitField('Guardar')
