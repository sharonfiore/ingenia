from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, logout_user, current_user, login_user, login_required

from app import login_manager
from app.auth import auth_bp
from app.auth.forms.LoginForm import LoginForm
from app.models import Usuario, Curso, CursoProgramado
from app.snippets import is_safe_url


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            u = Usuario.query.filter_by(username=username).first()
            if u:
                if u.check_password(password):
                    login_user(u, remember=True)
                    next = request.args.get('next')
                    if not is_safe_url(next):
                        return abort(400)
                    return redirect(next or url_for('dashboard.index'))
                else:
                    return render_template("auth/login_form.html", form=form)
            else:
                return render_template("auth/login_form.html", form=form)
        else:
            return render_template("auth/login_form.html", form=form)
    else:
        return render_template('auth/login_form.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))