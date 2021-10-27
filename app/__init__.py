from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    # Blueprints
    from .dashboard import dashboard_bp
    from .auth import auth_bp
    from .cursos import cursos_bp
    from .alumnos import alumnos_bp
    from .public import public_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(public_bp)

    with app.app_context():
        db.create_all()

    return app

