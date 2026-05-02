from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

views = Blueprint("pilihan_layanan", __name__)

@views.route("/pilihan-layanan")
@login_required
def pilihan_layanan():
    return render_template("pilihan-layanan.html", user=current_user)