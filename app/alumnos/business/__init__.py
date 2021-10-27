from app.models import CursoProgramado
from app import db
from datetime import datetime


def guardar_curso_programado(curso, fecha_ini):
    try:
        cp = CursoProgramado()
        cp.curso_id = curso.id
        cp.fecha_inicio = datetime.strptime(fecha_ini, '%d/%m/%Y') 
        db.session.add(cp)
        db.session.commit()
        return "El Curso fue programado exitósamente"
    except Exception as e:
        print(e)
        return None

def actualizar_curso_programado(pid, fecha_ini):
    try:
        cp = CursoProgramado.query.filter_by(id=pid).first()
        cp.fecha_inicio = datetime.strptime(fecha_ini, '%d/%m/%Y') 
        db.session.add(cp)
        db.session.commit()
        return "El Curso fue actualizado exitósamente"
    except Exception as e:
        print(e)
        return None
 