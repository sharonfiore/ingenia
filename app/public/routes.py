from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.models import AlumnoCurso, Alumno
from app.public import public_bp
from app.public.forms import BuscarCertForm
from flask import current_app, send_from_directory


@public_bp.route('/public/certificado/', methods=['GET'])
def certificado_busqueda():
    lista = []
    ndni = request.args.get('dni')
    if ndni:
        dni = ndni
        a = Alumno.query.filter_by(dni=dni).first()
        if a:
            lista = AlumnoCurso.query.filter_by(alumno_id=a.id).all()
            if not lista:
                flash("Estimado "+str(a.nombre.split(' ')[0].capitalize())+", tu certificado aún no esta disponible.")
                flash("Si gusta puede escribirnos a: informes@ingeniacyc.com")
                return render_template("public/buscar_certificado.html", alumno=a, lista=lista)

            return render_template("public/buscar_certificado.html", alumno=a, lista=lista)
        else:
            flash("El dni ingresado no está registrado en nuestro sistema")
            return render_template("public/buscar_certificado.html",alumno=a,lista=lista)

        return render_template("public/buscar_certificado.html", alumno=a, lista=lista)
    else:
        return render_template('public/buscar_certificado.html', alumno=None, lista=lista)

@public_bp.route('/public/certificado/<string:filename>', methods=['GET', 'POST'])
def download_cert(filename):
    try:
        return send_from_directory(current_app.config["REPO_CERTIFICADOS"],
                                   filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

