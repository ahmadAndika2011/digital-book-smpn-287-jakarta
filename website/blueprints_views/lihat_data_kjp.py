from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananKjp

views = Blueprint("lihat_data_kjp", __name__)

@views.route("/lihat-data-kjp/<int:id>")
@login_required
def lihat_data_kjp(id):
    data = DatabaseLayananKjp.query.get(id)
    return render_template("detail-data-layanan-kjp.html", item=data)