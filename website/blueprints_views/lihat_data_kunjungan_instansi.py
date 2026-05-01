from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananKunjunganAntarInstansi

views = Blueprint("lihat_data_kunjungan_instansi", __name__)

@views.route("/lihat-data-kunjungan_instansi/<int:id>")
def lihat_data_kunjungan_instansi(id):
    data = DatabaseLayananKunjunganAntarInstansi.query.get(id)
    return f"Hi {data.nama}"