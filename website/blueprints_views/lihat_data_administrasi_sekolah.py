from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananAdministrasiSekolah

views = Blueprint("lihat_data_administrasi_sekolah", __name__)

@views.route("/lihat-data-administrasi_sekolah/<int:id>")
def lihat_data_administrasi_sekolah(id):
    data = DatabaseLayananAdministrasiSekolah.query.get(id)
    return f"Hi {data.nama}"