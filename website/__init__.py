from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus
import os
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://andika:{quote_plus(os.getenv('DB_PASSWORD'))}@187.77.113.166/{os.getenv('DB_NAME')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    mail.init_app(app)

    app.config["UPLOADS_FOLDER"] = os.path.join(app.root_path, "uploads")
    os.makedirs(app.config["UPLOADS_FOLDER"], exist_ok=True)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .blueprints import login_siswa, login_admin, logout, input_data_siswa, update_data_siswa, update_data_per_siswa, buat_akun_siswa, input_berita, input_data_guru, upload_data_guru, update_data_guru, layanan_ppdb, layanan_mutasi, layanan_pip, layanan_kjp, layanan_administrasi_sekolah, layanan_kunjungan_antar_instansi, kontak
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
    app.register_blueprint(update_data_guru, url_prefix="/")
    app.register_blueprint(layanan_ppdb, url_prefix="/")
    app.register_blueprint(layanan_mutasi, url_prefix="/")
    app.register_blueprint(layanan_pip, url_prefix="/")
    app.register_blueprint(layanan_kjp, url_prefix="/")
    app.register_blueprint(layanan_administrasi_sekolah, url_prefix="/")
    app.register_blueprint(layanan_kunjungan_antar_instansi, url_prefix="/")
    app.register_blueprint(kontak, url_prefix="/")

    from .blueprints_views import dashbord_admin, pilihan_layanan, lihat_data_ppdb, lihat_data_mutasi, lihat_data_pip, lihat_data_kjp, lihat_data_administrasi_sekolah, lihat_data_kunjungan_instansi, hapus_data_ppdb, hapus_data_mutasi, hapus_data_pip, hapus_data_kjp, hapus_data_administrasi_sekolah, hapus_data_kunjungan_antar_instansi
    app.register_blueprint(dashbord_admin, url_prefix="/")
    app.register_blueprint(pilihan_layanan, url_prefix="/")
    app.register_blueprint(lihat_data_ppdb, url_prefix="/")
    app.register_blueprint(lihat_data_mutasi, url_prefix="/")
    app.register_blueprint(lihat_data_pip, url_prefix="/")
    app.register_blueprint(lihat_data_kjp, url_prefix="/")
    app.register_blueprint(lihat_data_administrasi_sekolah, url_prefix="/")
    app.register_blueprint(lihat_data_kunjungan_instansi, url_prefix="/")
    app.register_blueprint(hapus_data_ppdb, url_prefix="/")
    app.register_blueprint(hapus_data_mutasi, url_prefix="/")
    app.register_blueprint(hapus_data_pip, url_prefix="/")
    app.register_blueprint(hapus_data_kjp, url_prefix="/")
    app.register_blueprint(hapus_data_administrasi_sekolah, url_prefix="/")
    app.register_blueprint(hapus_data_kunjungan_antar_instansi, url_prefix="/")

    from .models import AdminAccount, DatabaseSiswa, NilaiSiswa, AccountSiswa, Berita, DatabaseGuru, DatabaseLayananPpdb, DatabaseLayananMutasi, DatabaseLayananPip, DatabaseLayananKjp, DatabaseLayananAdministrasiSekolah, DatabaseLayananKunjunganAntarInstansi, DatabaseKontakEmail
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return AdminAccount.query.get(int(id))

    return app