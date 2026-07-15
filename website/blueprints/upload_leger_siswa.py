from flask import Blueprint, render_template,  flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from ..models import DatabaseSiswa, DatabaseLegerSiswa
from datetime import datetime
from .. import db
import pandas as pd

auth = Blueprint("upload_leger_siswa", __name__)

ALLOWED_FORMAT = ["xlsx", "xls"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

@auth.route("upload-leger-siswa", methods=["GET", "POST"])
@login_required
def upload_leger_siswa():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                filename = secure_filename(file.filename)
                df = pd.read_excel(save_path)
                df = df.dropna(subset=['nama'])

                for index, row in df.iterrows():
                    cek_nama_siswa = DatabaseSiswa.query.filter_by(nisn=row["nisn"]).first()
                    if not cek_nama_siswa:
                        flash("Nama siswa belum ada di database", category="error")
                        return redirect(url_for("data_siswa.data_siswa"))
                    
                    cek_nama_siswa_from_nilai = DatabaseLegerSiswa.query.filter_by(nama=row["nama"]).first()
                    cek_nisn_siswa = DatabaseSiswa.query.filter_by(nisn=cek_nama_siswa.nisn).first()
                    if cek_nama_siswa_from_nilai:
                        flash("Nama siswa sudah ada di database", category="error")
                        continue
                    elif len(cek_nama_siswa.nisn) != 10:
                        flash("NISN harus terdiri dari 10 digit", category="error")
                        return redirect(url_for("data_siswa.data_siswa"))
                    elif not cek_nisn_siswa:
                        flash("NISN siswa belum ada di database", category="error")
                        return redirect(url_for("data_siswa.data_siswa"))
                    else:
                        nilai_siswa = DatabaseLegerSiswa(
                            nama = row["nama"],
                            nisn = cek_nama_siswa.nisn,
                            agama_kristen = f"{row["agama_kristen"]}",
                            agama_islam = f"{row["agama_islam"]}",
                            pkn = f"{row["pkn"]}",
                            b_indo = f"{row["b_indo"]}",
                            matematika = f"{row["matematika"]}",
                            ipa = f"{row["ipa"]}",
                            ips = f"{row["ips"]}",
                            b_inggris = f"{row["b_inggris"]}",
                            pjok = f"{row["pjok"]}",
                            informatika = f"{row["informatika"]}",
                            seni_budaya = f"{row["seni_budaya"]}",
                            sakit = f"{row["sakit"]}",
                            izin = f"{row["izin"]}",
                            alpha = f"{row["alpha"]}",
                            rohkris = f"{row["rohkris"]}",
                            rohis = f"{row["rohis"]}",
                            basket = f"{row["basket"]}",
                            takraw = f"{row["takraw"]}",
                            futsal = f"{row["futsal"]}",
                            silat = f"{row["silat"]}",
                            taekwondo = f"{row["taekwondo"]}",
                            pramuka = f"{row["pramuka"]}",
                            pmr = f"{row["pmr"]}",
                            marching_band = f"{row["marching_band"]}",
                        )
                        db.session.add(nilai_siswa)
                    
                flash("Success tambah Leger siswa", category="success")
                db.session.commit()

                os.remove(save_path)


        return redirect(url_for("data_siswa.data_siswa"))
    return render_template("upload-leger-siswa.html")