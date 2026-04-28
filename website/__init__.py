from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus
import os

db = SQLAlchemy()
DB_NAME = "smpn_287"
pw = quote_plus("4Hm@d-@Nd1k4")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Secret_Key_09182829291982"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://andika:{pw}@187.77.113.166/smpn_287"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.config["UPLOADS_FOLDER"] = os.path.join(app.root_path, "uploads")
    os.makedirs(app.config["UPLOADS_FOLDER"], exist_ok=True)

    from .views import views
    from .auth import auth
    from .blueprints import login_siswa, login_admin, logout, input_data_siswa, update_data_siswa, update_data_per_siswa, buat_akun_siswa, input_berita, input_data_guru, upload_data_guru
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(login_siswa, url_prefix="/")
    app.register_blueprint(login_admin, url_prefix="/")
    app.register_blueprint(logout, url_prefix="/")
    app.register_blueprint(input_data_siswa, url_prefix="/")
    app.register_blueprint(update_data_siswa, url_prefix="/")
    app.register_blueprint(update_data_per_siswa, url_prefix="/")
    app.register_blueprint(buat_akun_siswa, url_prefix="/")
    app.register_blueprint(input_berita, url_prefix="/")
    app.register_blueprint(input_data_guru, url_prefix="/")
    app.register_blueprint(upload_data_guru, url_prefix="/")

    from .models import AdminAccount, DatabaseSiswa, NilaiSiswa, AccountSiswa, ImgName, DataGuru
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return AdminAccount.query.get(int(id))

    return app