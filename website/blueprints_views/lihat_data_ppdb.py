from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananPpdb

views = Blueprint("lihat_data_ppdb", __name__)

@views.route("/lihat-data-ppdb/<int:id>")
@login_required
def lihat_data_ppdb(id):
    data = DatabaseLayananPpdb.query.get(id)
    return render_template("detail-data-layanan-ppdb.html", item=data)