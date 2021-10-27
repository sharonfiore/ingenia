from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from app.alumnos import alumnos_bp
from app.models import Alumno
from datetime import datetime
from app.alumnos.forms.register import UploadFromExcel
from app import db
from app.alumnos.forms.AlumnoForm import VerAlumnoForm
from flask import jsonify
import csv
from sqlalchemy import exc


@alumnos_bp.route('/alumnos/lista-completa')
@login_required
def lista_completa():
    if request.method == 'GET':
        op = request.args.get("op")
        if op == 'filtro-mixto':
            slug = request.args.get("slug").lower() 
            slug = "%{}%".format(slug)
            from sqlalchemy import or_
            lista = Alumno.query.filter(or_(Alumno.nombre.like(slug),
                                            Alumno.apellido.like(slug),
                                            Alumno.dni.like(slug),
                                            Alumno.correo.like(slug),
                                            Alumno.celular.like(slug),
                                            Alumno.slug.like(slug)
                                            )
                                        ).all()
            return jsonify([z.to_json() for z in lista])
        else:
            lista = Alumno.query.all()
            return render_template("alumnos/lista-completa.html", lista=lista)

@alumnos_bp.route('/alumnos/registrar-desde-excel', methods=['GET', 'POST'])
@login_required
def registrar_desde_excel():
    form = UploadFromExcel()
    if request.method == 'GET':
        return render_template("alumnos/registrar-desde-excel.html", form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            file = form.document.data
            data = file.stream.read().decode("ISO-8859-1")
            spamreader = csv.reader(data.splitlines())
            for row in spamreader:
                if len(row) > 0:
                    b = Alumno.query.filter(Alumno.dni == row[0]).first()
                    if not b:
                        if row[0] and row[1] and row[2] and row[3] and row[4] and row[5]:
                            a = Alumno()
                            a.dni = row[0].lower()
                            a.nombre = row[1].lower()
                            a.apellido = row[2].lower()
                            a.correo = row[3].lower()
                            a.celular = row[4].lower()
                            a.slug = row[5].lower()
                            db.session.add(a)
                            db.session.commit()
                        else:
                            flash("Algunos registros del CSV poseen campos no llenados") 
                    else:
                        flash("Se encontró en el CSV un dni que ya está registrado en la base de datos.") 
                else:
                    flash("El documento está vacio")

            flash("Los alumnos se registraron exitosamente")
            return render_template("alumnos/registrar-desde-excel.html", form=form)
        else:
            return render_template("alumnos/registrar-desde-excel.html", form=form)

@alumnos_bp.route('/alumnos/ver-alumno/<int:id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def ver_alumno(id):
    form = VerAlumnoForm()
    if request.method == 'GET':
        p = Alumno.query.filter_by(id=id).first() 
        form.id.data = p.id
        form.nombre.data = p.nombre
        form.apellido.data = p.apellido
        form.dni.data = p.dni
        form.correo.data = p.correo
        form.celular.data = p.celular
        form.slug.data = p.slug
        return render_template("alumnos/ver-alumno.html", form=form)
    elif request.method == 'POST':
        try:
            a = Alumno.query.filter_by(id=id).first()
            a.nombre = form.nombre.data.lower()
            a.apellido = form.apellido.data.lower()
            a.dni = form.dni.data
            a.correo = form.correo.data
            a.celular = form.celular.data
            a.slug = form.slug.data
            db.session.add(a)
            db.session.commit()
            flash("Datos actualizados exitosamente")
            return render_template("alumnos/ver-alumno.html", form=form)
        except Exception as e:
            error = 'Problema al guardar, verifique los datos ingresados'
            return render_template("alumnos/ver-alumno.html", form=form)
    elif request.method == 'DELETE':
        try:
            c = Alumno.query.get(id)
            db.session.delete(c)
            db.session.commit()
            lista = Alumno.query.all()
            return render_template("alumnos/lista-completa.html", lista=lista)
        except exc.IntegrityError:
            db.session.rollback()
            return "error"