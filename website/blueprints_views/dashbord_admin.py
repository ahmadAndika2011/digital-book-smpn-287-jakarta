from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

views = Blueprint("dashbord_admin", __name__)

@views.route("/dashbord-admin")
@login_required
def dashbord_admin():
    return render_template("dashbord-admin.html", user=current_user)