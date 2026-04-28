from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required

auth = Blueprint("logout", __name__)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_admin.login"))