from fileinput import filename
import re
from unicodedata import category
from click.utils import R
from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import file
from .models import AdminAccount, DatabaseSiswa, NilaiSiswa, AccountSiswa, ImgName, DataGuru
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
import os
from werkzeug.utils import secure_filename
import pandas as pd

auth = Blueprint("auth", __name__)

@auth.route("/choose-login")
def choose_login():
    return render_template("choose-login.html")

@auth.route("/login-siswa", methods=["GET", "POST"])
def login_siswa():
    if request.method == "POST":
        nis = request.form.get("nis")
        password = request.form.get("password")
        
        check_nis = AccountSiswa.query.filter_by(nis=nis).first()
        if check_nis:
            check_password_hashing = check_password_hash(check_nis.password, password)
            if check_password_hashing:
                name = DatabaseSiswa.query.filter_by(nis=check_nis.nis).first().nama.split()[0]
                lulus = DatabaseSiswa.query.filter_by(nis=check_nis.nis).first().lulus
                flash(f"Selamat Login.", category="success")
                return redirect(url_for("views.data_siswa", name=name, lulus=lulus))
            else:
                flash("Password salah!", category="error")
        else:
            flash("NIS tidak ada!", category="error")
    return render_template("login-siswa.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        check_user = AdminAccount.query.filter(
            (AdminAccount.username==username) &
            (AdminAccount.secret_pw==password)
        ).first()

        if check_user:
            login_user(check_user, remember=True)
            jam = datetime.now().hour
            if jam >= 1 and jam < 10:
                greating = "Selamat Pagi"
            elif jam >= 10 and jam < 14:
                greating = "Selamat Siang"
            else:
                greating = "Selamat Sore"
            flash(f"{greating} {check_user.username}", category="success")
            return redirect(url_for("views.data_siswa"))
        else:
            flash("Username dan Password Salah!", category="error")
            return redirect(url_for("auth.login"))

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
        # input data Murid
        gambar_file = request.files.get("gambar")
        if gambar_file:
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            gambar_input = filename
        else:
            gambar_input = None

        name_input = request.form.get("name")
        nisn_input = request.form.get("nisn")
        nis_input = request.form.get("nis")
        tanggal_lahir_input = request.form.get("tanggal_lahir")
        tempat_lahir_input = request.form.get("tempat_lahir")
        agama_input = request.form.get("agama")
        sekolah_asal_input = request.form.get("sekolah_asal")
        lulus_input = request.form.get("lulus")
        check_duplicate_nisn = DatabaseSiswa.query.filter_by(
            nisn=nisn_input).first()
        check_duplicate_nis = DatabaseSiswa.query.filter_by(
            nis=nis_input).first()
        # input Nilai Murid
        n_agama_input = request.form.get("n_agama")
        n_pancasila_input = request.form.get("n_pancasila")
        n_indonesia_input = request.form.get("n_indonesia")
        n_matematika_input = request.form.get("n_matematika")
        n_ipa_input = request.form.get("n_ipa")
        n_ips_input = request.form.get("n_ips")
        n_inggris_input = request.form.get("n_inggris")
        n_seni_budaya_input = request.form.get("n_seni_budaya")
        n_olahraga_input = request.form.get("n_olahraga")
        n_prakarya_input = request.form.get("n_prakarya")

        try:
            valid_date = datetime.strptime(tanggal_lahir_input, "%Y-%m-%d")
        except Exception as e:
            valid_date = None

        if check_duplicate_nisn:
            flash("NISN sudah ada.", category="error")
            pass
        elif check_duplicate_nis:
            flash("NIS sudah ada.", category="error")
            pass
        elif len(nisn_input) != 10:
            flash("NISN harus 10 digit.", category="error")
            pass
        elif len(nis_input) != 4:
            flash("NIS harus 4 digit.", category="error")
            pass
        elif not valid_date:
            flash("Tanggal lahir tidak valid.", category="error")
            pass
        else:
            data_siswa = DatabaseSiswa(
                image=gambar_input,
                nama=name_input,
                nisn=nisn_input,
                nis=nis_input,
                tanggal_lahir=tanggal_lahir_input,
                tempat_lahir=tempat_lahir_input,
                agama=agama_input,
                sekolah_asal=sekolah_asal_input,
                lulus=lulus_input.title()
            )
            nilai_siswa = NilaiSiswa(
                nisn=nisn_input,
                agama=n_agama_input,
                pancasila=n_pancasila_input,
                indonesia=n_indonesia_input,
                matematika=n_matematika_input,
                ipa=n_ipa_input,
                ips=n_ips_input,
                inggris=n_inggris_input,
                seni_budaya=n_seni_budaya_input,
                olahraga=n_olahraga_input,
                prakarya=n_prakarya_input
            )
            db.session.add(data_siswa)
            db.session.add(nilai_siswa)
            db.session.commit()
            flash("Berhasil tambah data.", user=current_user, category="success")

    return render_template("input.html")

ALLOWED_FORMAT = ["xlsx", "xls", "csv"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

@auth.route("/update-data/<int:id>", methods=["GET", "POST"])
@login_required
def update_data(id):
    student = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=student.nisn).first()

    if request.method == "POST":
        """
            data student
        """
        gambar_file = request.files.get("gambar")
        if gambar_file:
            # hapus gambar
            if student and student.image:
                image_path = os.path.join(
                    current_app.root_path, "static/uploads", student.image)
                if os.path.exists(image_path):
                    os.remove(image_path)

            # update gambar
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            student.image = filename
            flash("success update gambar.", category="success")
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")
        lulus_new = request.form.get("lulus")

        success_update = []

        if len(name_new) < 1:
            pass
        else:
            success_update.append("nama")
            student.nama = name_new
        if len(nisn_new) != 10:
            pass
        else:
            success_update.append("nisn")
            student.nisn = nisn_new
        if len(nis_new) != 4:
            pass
        else:
            success_update.append("nis")
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(
                tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        if not valid_tanggal_lahir:
            pass
        else:
            success_update.append("tanggal lahir")
            student.tanggal_lahir = tanggal_lahir_new

        if len(tempat_lahir_new) < 1:
            pass
        else:
            success_update.append("tempat lahir")
            student.tempat_lahir = tempat_lahir_new.title()
        if not agama_new:
            pass
        else:
            success_update.append("agama")
            student.agama = agama_new
        if len(sekolah_asal_new) < 1:
            pass
        else:
            success_update.append("sekolah asal")
            student.sekolah_asal = sekolah_asal_new
        if len(lulus_new) < 1:
            pass
        else:
            success_update.append("lulus")
            student.lulus = lulus_new.title()

        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(
                    f"success update {success_update[i]}.", category="success")

        """
            Nilai student
        """
        file = request.files.get("upload_nilai")

        if file and file.filename != "":
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                flash("Nilai berhasil disimpan.", category="success")
                filename = secure_filename(file.filename)
                if filename.endswith(".csv"):
                    df_nilai_siswa = pd.read_csv(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                else:
                    df_nilai_siswa = pd.read_excel(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                
                os.remove(save_path)
        else:
            n_agama_new = request.form.get("n_agama")
            n_pancasila_new = request.form.get("n_pancasila")
            n_indonesia_new = request.form.get("n_indonesia")
            n_matematika_new = request.form.get("n_matematika")
            n_ipa_new = request.form.get("n_ipa")
            n_ips_new = request.form.get("n_ips")
            n_inggris_new = request.form.get("n_inggris")
            n_seni_budaya_new = request.form.get("n_seni_budaya")
            n_olahraga_new = request.form.get("n_olahraga")
            n_prakarya_new = request.form.get("n_prakarya")

            success_update_n = []

            if len(n_agama_new) < 1:
                pass
            else:
                success_update_n.append("nilai agama")
                nilai_siswa.agama = n_agama_new

            if len(n_pancasila_new) < 1:
                pass
            else:
                success_update_n.append("nilai ppkn")
                nilai_siswa.pancasila = n_pancasila_new

            if len(n_indonesia_new) < 1:
                pass
            else:
                success_update_n.append("nilai bahasa indonesia")
                nilai_siswa.indonesia = n_indonesia_new

            if len(n_matematika_new) < 1:
                pass
            else:
                success_update_n.append("nilai matematika")
                nilai_siswa.matematika = n_matematika_new

            if len(n_ipa_new) < 1:
                pass
            else:
                success_update_n.append("nilai ipa")
                nilai_siswa.ipa = n_ipa_new

            if len(n_ips_new) < 1:
                pass
            else:
                success_update_n.append("nilai ips")
                nilai_siswa.ips = n_ips_new

            if len(n_inggris_new) < 1:
                pass
            else:
                success_update_n.append("nilai bahasa ingrris")
                nilai_siswa.inggris = n_inggris_new

            if len(n_seni_budaya_new) < 1:
                pass
            else:
                success_update_n.append("nilai seni budaya")
                nilai_siswa.seni_budaya = n_seni_budaya_new

            if len(n_olahraga_new) < 1:
                pass
            else:
                success_update_n.append("nilai olahraga")
                nilai_siswa.olahraga = n_olahraga_new

            if len(n_prakarya_new) < 1:
                pass
            else:
                success_update_n.append("nilai prakarya")
                nilai_siswa.prakarya = n_prakarya_new

            if len(success_update_n) >= 1:
                for i in range(len(success_update_n)):
                    flash(
                        f"success update {success_update_n[i]}.", category="success")

        db.session.commit()
        return redirect(url_for("views.data_siswa"))

    return render_template("update_data.html", user=current_user)


@auth.route("/update-data-per-student/<int:id>", methods=["GET", "POST"])
@login_required
def update_data_student(id):
    student = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=student.nisn).first()

    if request.method == "POST":
        """
            data student
        """
        gambar_file = request.files.get("gambar")
        if gambar_file:
            # hapus gambar
            if student and student.image:
                image_path = os.path.join(
                    current_app.root_path, "static/uploads", student.image)
                if os.path.exists(image_path):
                    os.remove(image_path)

            # update gambar
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            student.image = filename
            flash("success update gambar.", category="success")
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")
        lulus_new = request.form.get("lulus")

        success_update = []

        if len(name_new) < 1:
            pass
        else:
            success_update.append("nama")
            student.nama = name_new
        if len(nisn_new) != 10:
            pass
        else:
            success_update.append("nisn")
            student.nisn = nisn_new
        if len(nis_new) != 4:
            pass
        else:
            success_update.append("nis")
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(
                tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        if not valid_tanggal_lahir:
            pass
        else:
            success_update.append("tanggal lahir")
            student.tanggal_lahir = tanggal_lahir_new

        if len(tempat_lahir_new) < 1:
            pass
        else:
            success_update.append("tempat lahir")
            student.tempat_lahir = tempat_lahir_new.title()
        if not agama_new:
            pass
        else:
            success_update.append("agama")
            student.agama = agama_new
        if len(sekolah_asal_new) < 1:
            pass
        else:
            success_update.append("sekolah asal")
            student.sekolah_asal = sekolah_asal_new
        if len(lulus_new) < 1:
            pass
        else:
            success_update.append("lulus")
            student.lulus = lulus_new.title()

        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(
                    f"success update {success_update[i]}.", category="success")

        """
            nilai student
        """
        file = request.files.get("upload_nilai")
        if file and file.filename:
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                flash("Nilai berhasil disimpan.", category="success")
                filename = secure_filename(file.filename)
                if filename.endswith(".csv"):
                    df_nilai_siswa = pd.read_csv(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                else:
                    df_nilai_siswa = pd.read_excel(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                os.remove(save_path)
        else:
            n_agama_new = request.form.get("n_agama")
            n_pancasila_new = request.form.get("n_pancasila")
            n_indonesia_new = request.form.get("n_indonesia")
            n_matematika_new = request.form.get("n_matematika")
            n_ipa_new = request.form.get("n_ipa")
            n_ips_new = request.form.get("n_ips")
            n_inggris_new = request.form.get("n_inggris")
            n_seni_budaya_new = request.form.get("n_seni_budaya")
            n_olahraga_new = request.form.get("n_olahraga")
            n_prakarya_new = request.form.get("n_prakarya")

            success_update_n = []

            if len(n_agama_new) < 1:
                pass
            else:
                success_update_n.append("nilai agama")
                nilai_siswa.agama = n_agama_new

            if len(n_pancasila_new) < 1:
                pass
            else:
                success_update_n.append("nilai ppkn")
                nilai_siswa.pancasila = n_pancasila_new

            if len(n_indonesia_new) < 1:
                pass
            else:
                success_update_n.append("nilai bahasa indonesia")
                nilai_siswa.indonesia = n_indonesia_new

            if len(n_matematika_new) < 1:
                pass
            else:
                success_update_n.append("nilai matematika")
                nilai_siswa.matematika = n_matematika_new

            if len(n_ipa_new) < 1:
                pass
            else:
                success_update_n.append("nilai ipa")
                nilai_siswa.ipa = n_ipa_new

            if len(n_ips_new) < 1:
                pass
            else:
                success_update_n.append("nilai ips")
                nilai_siswa.ips = n_ips_new

            if len(n_inggris_new) < 1:
                pass
            else:
                success_update_n.append("nilai bahasa ingrris")
                nilai_siswa.inggris = n_inggris_new

            if len(n_seni_budaya_new) < 1:
                pass
            else:
                success_update_n.append("nilai seni budaya")
                nilai_siswa.seni_budaya = n_seni_budaya_new

            if len(n_olahraga_new) < 1:
                pass
            else:
                success_update_n.append("nilai olahraga")
                nilai_siswa.olahraga = n_olahraga_new

            if len(n_prakarya_new) < 1:
                pass
            else:
                success_update_n.append("nilai prakarya")
                nilai_siswa.prakarya = n_prakarya_new

            if len(success_update_n) >= 1:
                for i in range(len(success_update_n)):
                    flash(
                        f"success update {success_update_n[i]}.", category="success")

        db.session.commit()
        return redirect(url_for("views.info", id=id))

    return render_template("update_data.html", user=current_user)


@auth.route("/upload-file", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                flash("Data berhasil disimpan.", category="success")
                filename = secure_filename(file.filename)
                if filename.endswith(".csv"):
                    df_siswa = pd.read_csv(
                        save_path, dtype={"nis": str, "nisn": str})
                    df_siswa = df_siswa.fillna("")
                    for index, row in df_siswa.iterrows():
                        existing = DatabaseSiswa.query.filter_by(
                            nisn=row["nisn"]).first()

                        if existing:
                            flash(
                                f"{row['nama']} sudah ada di database.", category="error")
                            continue

                        if len(row["nis"].strip()) != 4:
                            flash(
                                f"{row['nama']} memiliki nis tidak sama dengan 4 digit.", category="error")
                            continue

                        if len(row["nisn"].strip()) != 10:
                            flash(
                                f"{row['nama']} memiliki nisn tidak sama dengan 10 digit.", category="error")
                            continue

                        try:
                            valid_tanggal_lahir = datetime.strptime(
                                row["tanggal_lahir"], "%Y-%m-%d")
                        except:
                            valid_tanggal_lahir = None
                            flash(
                                f"{row['nama']} memiliki format tanggal lahir yang salah.", category="error")
                            continue
                        data_siswa = DatabaseSiswa(
                            nama=row["nama"],
                            nisn=row["nisn"],
                            nis=row["nis"],
                            tanggal_lahir=row["tanggal_lahir"],
                            tempat_lahir=row["tempat_lahir"],
                            agama=row["agama"],
                            sekolah_asal=row["sekolah_asal"],
                            lulus=row["lulus"],
                        )
                        db.session.add(data_siswa)

                        nilai_siswa = NilaiSiswa(
                            nisn=row["nisn"],
                            agama="",
                            pancasila="",
                            indonesia="",
                            matematika="",
                            ipa="",
                            ips="",
                            inggris="",
                            seni_budaya="",
                            olahraga="",
                            prakarya="",
                        )
                        db.session.add(nilai_siswa)
                else:
                    df_siswa = pd.read_excel(
                        save_path, dtype={"nis": str, "nisn": str})
                    df_siswa = df_siswa.fillna("")

                    for index, row in df_siswa.iterrows():
                        existing = DatabaseSiswa.query.filter_by(
                            nisn=row["nisn"]).first()
                        if existing:
                            flash(
                                f"{row['nama']} sudah ada di database.", category="error")
                            continue

                        if len(row["nis"].strip()) != 4:
                            flash(
                                f"{row['nama']} memiliki nis tidak sama dengan 4 digit.", category="error")
                            continue

                        if len(row["nisn"].strip()) != 10:
                            flash(
                                f"{row['nama']} memiliki nisn tidak sama dengan 10 digit.", category="error")
                            continue

                        try:
                            valid_tanggal_lahir = datetime.strptime(
                                row["tanggal_lahir"], "%Y-%m-%d")
                        except:
                            valid_tanggal_lahir = None
                            flash(
                                f"{row['nama']} memiliki format tanggal lahir yang salah.", category="error")
                            continue

                        data_siswa = DatabaseSiswa(
                            nama=row["nama"],
                            nisn=row["nisn"],
                            nis=row["nis"],
                            tanggal_lahir=row["tanggal_lahir"],
                            tempat_lahir=row["tempat_lahir"],
                            agama=row["agama"],
                            sekolah_asal=row["sekolah_asal"],
                            lulus=row["lulus"],
                        )
                        db.session.add(data_siswa)

                        nilai_siswa = NilaiSiswa(
                            nisn=row["nisn"],
                            agama="",
                            pancasila="",
                            indonesia="",
                            matematika="",
                            ipa="",
                            ips="",
                            inggris="",
                            seni_budaya="",
                            olahraga="",
                            prakarya="",
                        )
                        db.session.add(nilai_siswa)
                db.session.commit()
                # ? Remove kembali file
                os.remove(save_path)
                return redirect(url_for("views.data_siswa"))
            else:
                flash("Format Tidak diizinkan", category="error")
        else:
            flash("Tidak ada file yang disimpan", category="error")
    return render_template("upload_file.html", user=current_user)


@auth.route("/buat-akun", methods=["GET", "POST"])
def buat_akun():
    if request.method == "POST":
        nis = request.form.get("nis")
        password = request.form.get("password")
        check_nis = DatabaseSiswa.query.filter_by(nis=nis).first()
        check_nis_from_account = AccountSiswa.query.filter_by(nis=nis).first()
        if check_nis:
            if not check_nis_from_account:
                if password:
                    hash_password = generate_password_hash(password, method="pbkdf2:sha256")
                    account_siswa = AccountSiswa(
                        nis=nis,
                        password=hash_password
                    )
                    db.session.add(account_siswa)
                    db.session.commit()
                    flash("Akun berhasil dibuat!", category="success")
                    return redirect(url_for('auth.buat_akun'))
                else:
                    flash("Password tidak boleh kosong!", category="error")
                    return redirect(url_for('auth.buat_akun'))
            else:
                flash("Akun untuk NIS ini sudah ada!", category="error")
                return redirect(url_for('auth.buat_akun'))
        else:
            flash("NIS tidak ditemukan di database!", category="error")
            return redirect(url_for('auth.buat_akun'))
        
    return render_template("buat-akun.html")

@auth.route("/tambah-berita", methods=["GET", "POST"])
@login_required
def tambah_berita():
    if request.method == "POST":
        gambar_1_file = request.files.get("gambar_1")
        if gambar_1_file:
            filename = secure_filename(gambar_1_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_1_file.save(os.path.join(upload_path, filename))
            gambar_1_input = filename
        else:
            gambar_1_input = None
            
        gambar_2_file = request.files.get("gambar_2")
        if gambar_2_file:
            filename = secure_filename(gambar_2_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_2_file.save(os.path.join(upload_path, filename))
            gambar_2_input = filename
        else:
            gambar_2_input = ""

        gambar_3_file = request.files.get("gambar_3")
        if gambar_3_file:
            filename = secure_filename(gambar_3_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_3_file.save(os.path.join(upload_path, filename))
            gambar_3_input = filename
        else:
            gambar_3_input = ""

        video = request.files.get("video")
        if video:
            filename = secure_filename(video.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            video.save(os.path.join(upload_path, filename))
            video_input = filename
        else:
            video_input = ""

        text_input = request.form.get("keterangan")

        if text_input:
            input_berita = ImgName(
                name = text_input,
                img_1 = gambar_1_input,
                img_2 = gambar_2_input,
                img_3 = gambar_3_input,
                video = video_input
            )
            db.session.add(input_berita)
            db.session.commit()
            flash("Success Tambah berita.", category="success")
            return redirect(url_for("views.home"))

    return render_template("input-berita.html")


@auth.route("/tambah-data-guru", methods=["GET", "POST"])
@login_required
def tambah_data_guru():
    if request.method == "POST":
        gambar_file = request.files.get("gambar")
        if gambar_file:
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join(upload_path, filename))
            gambar_file_input = filename
        else:
            gambar_file_input = None

        name_input = request.form.get("name")
        mapel_input = request.form.get("mapel")
        nip_input = request.form.get("nip")
        status_input = request.form.get("status")
        jabatan_input = request.form.get("jabatan")
        tahun_masuk_input = request.form.get("tahun_masuk")

        if name_input and (len(nip_input) == 0 or len(nip_input) == 18):
            data_guru = DataGuru(
                name = name_input,
                image=gambar_file_input,
                mapel=mapel_input,
                nip=nip_input,
                status=status_input,
                jabatan=jabatan_input,
                tahun_masuk=tahun_masuk_input
            )
            db.session.add(data_guru)
            db.session.commit()
            flash("Success tambah data guru", category="success")
            return redirect(url_for("auth.tambah_data_guru"))
        else:
            flash("Jika NIP tidak lengkap maka bisa dikosongkan untuk mencegah kesalahan", category="error")
    return render_template("tambah-data-guru.html", user=current_user)