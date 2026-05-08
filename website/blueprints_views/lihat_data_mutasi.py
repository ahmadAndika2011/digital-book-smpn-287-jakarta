from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananMutasi
from ..views import role_required

views = Blueprint("lihat_data_mutasi", __name__)

@views.route("/lihat-data-mutasi/<int:id>")
@login_required
@role_required("superadmin", "layanan")
def lihat_data_mutasi(id):
    data = DatabaseLayananMutasi.query.get(id)
    return render_template("detail-data-layanan-mutasi.html", item=data)