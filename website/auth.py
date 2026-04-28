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

ALLOWED_FORMAT = ["xlsx", "xls", "csv"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

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
                filename = secure_filename(file.filename)
                if filename.endswith(".csv"):
                    df_siswa = pd.read_csv(
                        save_path, dtype={"nis": str, "nisn": str})
                    df_siswa = df_siswa.fillna("")

                    list_error_update = []

                    for index, row in df_siswa.iterrows():
                        db.session.rollback() 
                        existing = DatabaseSiswa.query.filter_by(
                            nisn=row["nisn"]).first()

                        if existing:
                            list_error_update.append(row["nama"])
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
                            alamat=row["alamat"],
                            rt=row["rt"],
                            rw=row["rw"],
                            kelurahan=row["kelurahan"],
                            kecamatan=row["kecamatan"],
                            sekolah_asal=row["sekolah_asal"],
                            lulus=row["lulus"],
                        )

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
                        try:
                            db.session.add(data_siswa)
                            db.session.add(nilai_siswa)
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            list_error_update.append(f"{row['nama']} (gagal simpan)")
                            continue
                else:
                    df_siswa = pd.read_excel(
                        save_path, dtype={"nis": str, "nisn": str})
                    df_siswa = df_siswa.fillna("")

                    list_error_update = []

                    for index, row in df_siswa.iterrows():
                        db.session.rollback() 
                        existing = DatabaseSiswa.query.filter_by(nisn=str(row["nisn"]).strip()).first()
                        if existing:
                            list_error_update.append(f"{row["nama"]}")
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
                            alamat=row["alamat"],
                            rt=row["rt"],
                            rw=row["rw"],
                            kelurahan=row["kelurahan"],
                            kecamatan=row["kecamatan"],
                            sekolah_asal=row["sekolah_asal"],
                            lulus=row["lulus"],
                        )

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
                        try:
                            db.session.add(data_siswa)
                            db.session.add(nilai_siswa)
                            db.session.commit()  # commit per siswa, dalam try/except
                        except Exception as e:
                            db.session.rollback()
                            list_error_update.append(f"{row['nama']} (gagal simpan)")
                            continue
                # ? Remove kembali file
                os.remove(save_path)

                for name in list_error_update:
                    flash(f"{name} sudah ada di database", category="error")
                return redirect(url_for("views.data_siswa"))
            else:
                flash("Format Tidak diizinkan", category="error")
        else:
            flash("Tidak ada file yang disimpan", category="error")
    return render_template("upload_file.html", user=current_user)

