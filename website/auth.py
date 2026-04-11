from flask import Blueprint, render_template, redirect, request_started, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import SecretPassword, DatabaseSiswa
from datetime import datetime
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password")

        user = SecretPassword.query.filter(
            (SecretPassword.secret_pw_1 == pw) |
            (SecretPassword.secret_pw_2 == pw)
        ).first()

        if user:
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            return redirect(url_for('views.home'))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/input", methods=["GET", "POST"])
@login_required
def input():
    if request.method == "POST":
        name_input = request.form.get("name")
        nisn_input = request.form.get("nisn")
        nis_input = request.form.get("nis")
        tanggal_lahir_input = request.form.get("tanggal_lahir")
        alamat_input = request.form.get("alamat")
        no_hp_input = request.form.get("no_hp")
        kelas_input = request.form.get("kelas")

        try:
            valid_date = datetime.strptime(tanggal_lahir_input, "%Y-%m-%d")
        except Exception as e:
            valid_date = None

        if len(name_input) < 1:
            pass
        elif len(nisn_input) != 10:
            pass
        elif len(nis_input) != 4:
            pass
        elif not valid_date:
            pass
        else:
            data_siswa = DatabaseSiswa(
                name=name_input, 
                nisn=nisn_input, 
                nis=nis_input, 
                tanggal_lahir=tanggal_lahir_input,
                alamat=alamat_input, 
                no_hp=no_hp_input, 
                kelas=kelas_input
            )
            db.session.add(data_siswa)
            db.session.commit()

    return render_template("input.html")

@auth.route("/update-data/<int:id>", methods=["GET", "POST"])
@login_required
def update_data(id):
    student = DatabaseSiswa.query.get(id)

    if request.method == "POST":
        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        alamat_new = request.form.get("alamat")
        no_hp_new = request.form.get("no_hp")
        kelas_new = request.form.get("kelas")

        # Check name
        if len(name_new) < 1:
            pass
        else:
            student.name = name_new

        # Check nisn
        if len(nisn_new) != 10:
            pass
        else:
            student.nisn = nisn_new

        # Check nis
        if len(nis_new) != 4:
            pass
        else:
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        # Check tanggal lahir
        if not valid_tanggal_lahir:
            pass
        else:
            student.tanggal_lahir = tanggal_lahir_new

        # Check alamat
        if len(alamat_new) < 1:
            pass
        else:
            student.alamat = alamat_new

        # Check no hp
        if len(no_hp_new) < 1:
            pass
        else:
            student.no_hp = no_hp_new

        # Check kelas
        if len(kelas_new) < 1:
            pass
        else:
            student.kelas = kelas_new
        
        db.session.commit()
        return redirect(url_for("views.home"))

    return render_template("update_data.html", user=current_user)