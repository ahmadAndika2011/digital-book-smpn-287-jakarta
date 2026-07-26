from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus
import os
from flask_mail import Mail
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_talisman import Talisman

load_dotenv()

db = SQLAlchemy()
mail = Mail()
talisman = Talisman()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production'
    app.config["PREFERRED_URL_SCHEME"] = 'https' if IS_PRODUCTION else 'http'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION 
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://root:@localhost/database_smpn_287"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://root:{quote_plus(os.getenv('DB_PASSWORD'))}@202.155.19.242/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    mail.init_app(app)

    csp = {
    'default-src': ["'self'"],
    
    'script-src': [
        "'self'",
        "'unsafe-inline'",       # Untuk inline script
        "cdn.jsdelivr.net",      # Bootstrap JS / Alpine.js
        "cdnjs.cloudflare.com",  # Library lain
    ],
    
    'style-src': [
        "'self'",
        "'unsafe-inline'",       # Untuk inline style
        "cdn.jsdelivr.net",      # Bootstrap CSS
        "fonts.googleapis.com",  # Google Fonts CSS
    ],
    
    'font-src': [
        "'self'",
        "fonts.gstatic.com",     # Google Fonts file
        "cdn.jsdelivr.net",
        "data:",
    ],
    
    'img-src': [
        "'self'",
        "data:",                 # Base64 image
        "*",                     # Semua sumber gambar
    ],
    
    'connect-src': ["'self'"],
} 
    # if IS_PRODUCTION else None

    talisman.init_app(app, force_https=IS_PRODUCTION, content_security_policy=csp)

    app.config["UPLOADS_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
    os.makedirs(app.config["UPLOADS_FOLDER"], exist_ok=True)

    # @app.errorhandler(Exception)
    # def redirecting(e):
    #     return render_template("error-page.html")

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .blueprints import login_siswa, tambah_file_arsip, layanan_kjp_baru, tambah_arsip_ijazah, login_admin, logout, tambah_arsip_guru, upload_leger_siswa, input_data_siswa, update_data_siswa, update_data_per_siswa, buat_akun_siswa, input_berita, input_data_guru, upload_data_guru, update_data_guru, layanan_ppdb, layanan_mutasi, layanan_pip, layanan_kjp, layanan_administrasi_sekolah, layanan_kunjungan_antar_instansi, kontak, feedbacks, jawab_feedback, tambah_nilai_siswa, upload_nilai_siswa, input_data_tendik, update_data_tendik, upload_data_tendik
    app.register_blueprint(tambah_arsip_ijazah, url_prefix="/")
    app.register_blueprint(layanan_kjp_baru, url_prefix="/")
    app.register_blueprint(tambah_file_arsip, url_prefix="/")
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
    app.register_blueprint(feedbacks, url_prefix="/")
    app.register_blueprint(jawab_feedback, url_prefix="/")
    app.register_blueprint(tambah_nilai_siswa, url_prefix="/")
    app.register_blueprint(upload_nilai_siswa, url_prefix="/")
    app.register_blueprint(input_data_tendik, url_prefix="/")
    app.register_blueprint(update_data_tendik, url_prefix="/")
    app.register_blueprint(upload_data_tendik, url_prefix="/")
    app.register_blueprint(upload_leger_siswa, url_prefix="/")
    app.register_blueprint(tambah_arsip_guru, url_prefix="/")

    from .blueprints_views import dashbord_admin, hapus_data_kjp_baru, table_kjp_baru, hapus_data_arsip_ijazah, arsip_ijazah, pilih_arsip_ijazah, hapus_data_arsip_guru, hapus_arsip_guru, detail_arsip_guru, arsip_guru, data_tendik, pilihan_layanan, lihat_data_ppdb, lihat_data_mutasi, lihat_data_pip, lihat_data_kjp, lihat_data_administrasi_sekolah, lihat_data_kunjungan_instansi, hapus_data_ppdb, hapus_data_mutasi, hapus_data_pip, hapus_data_kjp, hapus_data_administrasi_sekolah, hapus_data_kunjungan_antar_instansi, data_siswa, detail_siswa, data_guru, data_berita, template_lulus, detail_berita, detail_guru, hapus_berita, hapus_guru, hapus_siswa, table_kjp, data_feedbacks_user, hapus_feedback, detail_tendik, hapus_tendik
    app.register_blueprint(hapus_data_kjp_baru, url_prefix="/")
    app.register_blueprint(table_kjp_baru, url_prefix="/")
    app.register_blueprint(hapus_data_arsip_ijazah, url_prefix="/")
    app.register_blueprint(arsip_ijazah, url_prefix="/")
    app.register_blueprint(pilih_arsip_ijazah, url_prefix="/")
    app.register_blueprint(hapus_data_arsip_guru, url_prefix="/")
    app.register_blueprint(detail_arsip_guru, url_prefix="/")
    app.register_blueprint(hapus_arsip_guru, url_prefix="/")
    app.register_blueprint(arsip_guru, url_prefix="/")
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
    app.register_blueprint(data_siswa, url_prefix="/")
    app.register_blueprint(detail_siswa, url_prefix="/")
    app.register_blueprint(data_guru, url_prefix="/")
    app.register_blueprint(data_berita, url_prefix="/")
    app.register_blueprint(template_lulus, url_prefix="/")
    app.register_blueprint(detail_berita, url_prefix="/")
    app.register_blueprint(detail_guru, url_prefix="/")
    app.register_blueprint(hapus_berita, url_prefix="/")
    app.register_blueprint(hapus_guru, url_prefix="/")
    app.register_blueprint(hapus_siswa, url_prefix="/")
    app.register_blueprint(table_kjp, url_prefix="/")
    app.register_blueprint(data_feedbacks_user, url_prefix="/")
    app.register_blueprint(hapus_feedback, url_prefix="/")
    app.register_blueprint(data_tendik, url_prefix="/")
    app.register_blueprint(detail_tendik, url_prefix="/")
    app.register_blueprint(hapus_tendik, url_prefix="/")

    from .models import AdminAccount, DatabaseLayananKjpBaru, DatabaseArsipIjazah, DatabaseSiswa, DatabaseLegerSiswa, DatabaseNilaiSiswa, AccountSiswa, Berita, DatabaseGuru, DatabaseLayananPpdb, DatabaseLayananMutasi, DatabaseLayananPip, DatabaseLayananKjp, DatabaseLayananAdministrasiSekolah, DatabaseLayananKunjunganAntarInstansi, DatabaseKontakEmail, DatabaseFeedbacks
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'login_admin.login_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return AdminAccount.query.get(int(id))

    return app