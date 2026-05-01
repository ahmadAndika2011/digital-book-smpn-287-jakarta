from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananMutasi

views = Blueprint("lihat_data_mutasi", __name__)

@views.route("/lihat-data-mutasi/<int:id>")
def lihat_data_mutasi(id):
    data = DatabaseLayananMutasi.query.get(id)
    return f"Hi {data.nama}"