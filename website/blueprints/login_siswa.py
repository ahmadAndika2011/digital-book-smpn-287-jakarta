from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import AccountSiswa, DatabaseSiswa
from werkzeug.security import check_password_hash

auth = Blueprint("login_siswa", __name__)

@auth.route("/cek-kelulusan-siswa", methods=["GET", "POST"])
def login_siswa():
    if request.method == "POST":
        nis = request.form.get("nis")
        password = request.form.get("password")
        
        check_nis = AccountSiswa.query.filter_by(nis=nis).first()
        if check_nis:
            check_password_hashing = check_password_hash(check_nis.password, password)
            if check_password_hashing:
                name = DatabaseSiswa.query.filter_by(nis=check_nis.nis).first().nama
                lulus = DatabaseSiswa.query.filter_by(nis=check_nis.nis).first().lulus
                flash(f"Selamat Login.", category="success")
                return redirect(url_for("views.template_lulus", name=name, lulus=lulus))
            else:
                flash("Password salah!", category="error")
        else:
            flash("NIS tidak ada!", category="error")
    return render_template("cek-kelulusan-siswa.html")