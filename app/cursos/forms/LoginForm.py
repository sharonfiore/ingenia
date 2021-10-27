from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="Ingresa un nombre de usuario válido"), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Ingresa una contraseña")]) 
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Ingresar')
