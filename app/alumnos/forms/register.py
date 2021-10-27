from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadFromExcel(FlaskForm):
    document = FileField('document', 
                         validators=[FileRequired('Debe subir un documento'),
                                     FileAllowed(['csv'], 
                                                 'El documento debe ser formato CSV')])
    submit = SubmitField('Registrar ahora')

class UploadFromPDF(FlaskForm):
    document = FileField('document', 
                         validators=[FileRequired('Debe subir un documento'),
                                     FileAllowed(['pdf'],
                                                 'El documento debe ser formato PDF')])
    submit = SubmitField('Subir ahora')
