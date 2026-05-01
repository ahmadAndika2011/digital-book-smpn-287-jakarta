from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananPpdb, DatabaseLayananMutasi, DatabaseLayananPip, DatabaseLayananKjp, DatabaseLayananAdministrasiSekolah, DatabaseLayananKunjunganAntarInstansi

views = Blueprint("dashbord_admin", __name__)

@views.route("/dashbord-admin")
@login_required
def dashbord_admin():
    data_layanan_ppdb = DatabaseLayananPpdb.query.all()
    data_layanan_mutasi = DatabaseLayananMutasi.query.all()
    data_layanan_pip = DatabaseLayananPip.query.all()
    data_layanan_kjp = DatabaseLayananKjp.query.all()
    data_layanan_administrasi_sekolah = DatabaseLayananAdministrasiSekolah.query.all()
    data_layanan_kunjungan_antar_instansi = DatabaseLayananKunjunganAntarInstansi.query.all()
    return render_template("dashbord-admin.html", 
                           user=current_user, 
                           data_layanan_ppdb=data_layanan_ppdb, 
                           data_layanan_mutasi=data_layanan_mutasi,
                           data_layanan_pip=data_layanan_pip,
                           data_layanan_kjp=data_layanan_kjp,
                           data_layanan_administrasi_sekolah=data_layanan_administrasi_sekolah,
                           data_layanan_kunjungan_antar_instansi=data_layanan_kunjungan_antar_instansi
                           )