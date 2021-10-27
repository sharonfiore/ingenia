from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.dashboard import dashboard_bp

@dashboard_bp.route('/')
@login_required
def index():
    if request.method == 'GET':
        return render_template("dashboard/index.html")