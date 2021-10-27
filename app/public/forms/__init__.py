from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class BuscarCertForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired(message="Ingresa un número de dni"), Length(max=8)])
