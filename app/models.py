from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def update_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return Usuario.query.get(id)


class Curso(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)


class CursoProgramado(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    curso = db.relationship("Curso", lazy='select')


class Alumno(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(12), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    celular = db.Column(db.String(12), nullable=False)
    slug = db.Column(db.String(12), nullable=False)

    def to_json(self):
        return {
            "id": int(self.id),
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "correo": self.correo,
            "celular": self.celular,
            "slug": self.slug
        }


class AlumnoCurso(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), nullable=False)
    curso_prog_id = db.Column(db.Integer, db.ForeignKey('curso_programado.id'), nullable=False)
    certificado = db.Column(db.Text, nullable=True)
    alumno = db.relationship("Alumno", lazy='select')
    curso_prog = db.relationship("CursoProgramado", lazy='select')
