from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import AdminAccount
from flask_login import login_user
from datetime import datetime
from werkzeug.security import check_password_hash

auth = Blueprint("login_admin", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        check_user = AdminAccount.query.filter(
            (AdminAccount.username==username)
        ).first()

        if check_user and check_password_hash(check_user.secret_pw, password):
            login_user(check_user, remember=True)
            jam = datetime.now().hour
            if jam >= 1 and jam < 10:
                greating = "Selamat Pagi"
            elif jam >= 10 and jam < 14:
                greating = "Selamat Siang"
            else:
                greating = "Selamat Sore"
            flash(f"{greating} {check_user.username}", category="success")
            # return redirect(url_for("views.data_siswa"))
            if check_user.role == 'limited':
                return redirect(url_for("views.home"))  # langsung ke sini
            else:
                return redirect(url_for("views.home"))
        else:
            flash("Username dan Password Salah!", category="error")
            return redirect(url_for("login_admin.login_page"))

    return render_template("login.html")