from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "smpn_287"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Secret_Key_09182829291982"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://root:@localhost/{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import SecretPassword, DatabaseSiswa
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return SecretPassword.query.get(int(id))

    return app