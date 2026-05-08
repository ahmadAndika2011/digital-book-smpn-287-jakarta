from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananAdministrasiSekolah
from ..views import role_required

views = Blueprint("lihat_data_administrasi_sekolah", __name__)

@views.route("/lihat-data-administrasi_sekolah/<int:id>")
@login_required
@role_required("superadmin")
def lihat_data_administrasi_sekolah(id):
    data = DatabaseLayananAdministrasiSekolah.query.get(id)
    return render_template("detail-data-layanan-administrasi-sekolah.html", item=data)