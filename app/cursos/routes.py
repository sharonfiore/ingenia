from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app import login_manager
from app.cursos import cursos_bp
from .forms.LoginForm import LoginForm
from .forms.CursosForm import ProgramarCursoForm, VerCursoForm
from app.models import Usuario, Curso, CursoProgramado, AlumnoCurso
from app.snippets import is_safe_url
from datetime import datetime
from flask import jsonify
from app.cursos.business import guardar_curso_programado, actualizar_curso_programado
from app import db
from app.alumnos.forms.register import UploadFromPDF
from werkzeug.utils import secure_filename
import os
import uuid
from flask import current_app
from flask import send_from_directory


@cursos_bp.route('/cursos/cursos-disponibles') 
@login_required
def cursos_disponibles():
    if request.method == 'GET':
        lista_cursos = Curso.query.all()
        return render_template("cursos/cursos-disponibles.html", lista_cursos=lista_cursos)

@cursos_bp.route('/cursos/cursos-programados', methods=['GET', 'DELETE', 'PUT'])
@login_required
def cursos_programados():
    if request.method == 'GET':
        lista_cursos = CursoProgramado.query.order_by(CursoProgramado.fecha_inicio.asc()).all()
        return render_template("cursos/cursos-programados.html", lista_cursos=lista_cursos)
    elif request.method == 'DELETE':
        content = request.get_json(force = True)
        c = CursoProgramado.query.get(int(content['id']))
        db.session.delete(c)
        db.session.commit()
        lista_cursos = CursoProgramado.query.order_by(CursoProgramado.fecha_inicio.asc()).all()
        return render_template("cursos/cursos-programados.html", lista_cursos=lista_cursos)
    elif request.method == 'PUT':
        data = request.get_json(force = True)["params"]
        if data["op"] == 'inscribir-alumnos':
            print(data)
            ids = data["ids"]
            for id in ids:
                ex = AlumnoCurso.query.filter(AlumnoCurso.alumno_id==id,
                                              AlumnoCurso.curso_prog_id==data["cid"]).first()

                if not ex:
                    c = AlumnoCurso()
                    c.alumno_id = id
                    c.curso_prog_id = data["cid"]
                    db.session.add(c)
                    db.session.commit()
            return jsonify({"message": "ok"})

@cursos_bp.route('/cursos/cursos-programados/descargar-certificado/<string:filename>', methods=['GET', 'POST'])
@login_required
def download_file(filename): 
    try:
        return send_from_directory(current_app.config["REPO_CERTIFICADOS"], 
                                   filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@cursos_bp.route('/cursos/cursos-programados/<int:cid>/alumno/<int:aid>/subir-certificado', methods=['GET', 'POST'])
@login_required
def curso_alumno_subir_certificado(cid, aid):
    form = UploadFromPDF()
    if request.method == 'GET':
        return render_template("cursos/subir-certificado.html", form=form, cid=cid, aid=aid)
    elif request.method == 'POST':
        if form.validate_on_submit():
            id_pdf = uuid.uuid1().time
            file = form.document.data
            filename = str(id_pdf)+str(".pdf")
            filedir = os.path.join(current_app.config["REPO_CERTIFICADOS"], filename)
            print(filedir)
            file.save(filedir)
            cp = AlumnoCurso.query.filter_by(alumno_id=aid, curso_prog_id=cid).first()
            cp.certificado = filename
            db.session.merge(cp)
            db.session.commit()
            flash("Certificado registrado exitosamente")
            return render_template("cursos/subir-certificado.html", form=form, cid=cid, aid=aid)
        else:
            return render_template("cursos/subir-certificado.html", form=form, cid=cid, aid=aid)

@cursos_bp.route('/cursos/cursos-programados/<int:id>', methods=['GET', 'POST'])
@login_required
def ver_curso_programado(id):
    form = VerCursoForm()
    if request.method == 'GET':
        p = CursoProgramado.query.filter_by(id=id).first()
        lista = AlumnoCurso.query.filter_by(curso_prog_id=p.id).all()
        form.id.data = p.id
        form.curso.data = p.curso.nombre
        form.fecha_ini.data = datetime.strftime(p.fecha_inicio, '%d/%m/%Y')
        return render_template("cursos/ver-curso-programado.html", form=form, lista=lista)
    elif request.method == 'POST':
        message = actualizar_curso_programado(form.id.data, form.fecha_ini.data)
        lista = AlumnoCurso.query.filter_by(curso_prog_id=form.id.data).all()
        if message:
            flash(message)
            return render_template("cursos/ver-curso-programado.html", form=form, lista=lista)
        else:
            error = 'Problema al guardar, verifique los datos ingresados'
            return render_template("cursos/ver-curso-programado.html", form=form, lista=lista, error=error)

        return render_template("cursos/ver-curso-programado.html", form=form, lista=lista)

@cursos_bp.route('/cursos/programar-curso', methods=['GET', 'POST'])
@login_required
def programar_curso():
    form = ProgramarCursoForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            curso = form.curso.data
            fecha_ini = form.fecha_ini.data
            fecha_fin = form.fecha_fin.data
            message = guardar_curso_programado(curso, fecha_ini, fecha_fin)
            if message:
                flash(message)
                return render_template("cursos/programar-curso.html", form=form)
            else:
                error = 'Problema al guardar, verifique los datos ingresados'
                return render_template("cursos/programar-curso.html", form=form, error=error)
        else:
            return render_template("cursos/programar-curso.html", form=form)
    else:
        lista_cursos = Curso.query.all()
        return render_template("cursos/programar-curso.html", lista_cursos=lista_cursos, form=form)

@cursos_bp.route('/cursos/alumnos-registrados', methods=['GET', 'DELETE'])
@login_required
def alumnos_registrados():
    if request.method == 'DELETE': 
        id = request.args.get('id') 
        a = AlumnoCurso.query.get(int(id))
        db.session.delete(a)
        db.session.commit()
        return {"message": "ok"}
