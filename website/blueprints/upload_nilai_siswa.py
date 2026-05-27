from flask import Blueprint, render_template,  flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from ..models import DatabaseSiswa, DatabaseNilaiSiswa
from datetime import datetime
from .. import db
import pandas as pd

auth = Blueprint("upload_nilai_siswa", __name__)

ALLOWED_FORMAT = ["xlsx", "xls"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

@auth.route("upload-nilai-siswa", methods=["GET", "POST"])
def upload_nilai_siswa():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                filename = secure_filename(file.filename)
                df = pd.read_excel(save_path)
                new_df = df[["Nama Siswa", "Rata-Rata", "Rata-Rata.1", "Rata-Rata.2", "Rata-Rata.3", "Rata-Rata.4", "Rata-Rata.5", "Rata-Rata.6", "Rata-Rata.7", "Rata-Rata.8", "Rata-Rata.9"]].dropna().reset_index(drop=True)
                new_df = new_df.rename(columns={
                    "Rata-Rata": "pkn",
                    "Rata-Rata.1": "b_indonesia",
                    "Rata-Rata.2": "matematika",
                    "Rata-Rata.3": "ipa",
                    "Rata-Rata.4": "ips",
                    "Rata-Rata.5": "b_inggris",
                    "Rata-Rata.6": "agama",
                    "Rata-Rata.7": "pjok",
                    "Rata-Rata.8": "tik",
                    "Rata-Rata.9": "seni_tari",
                })

                for index, row in new_df.iterrows():
                    cek_nama_siswa = DatabaseSiswa.query.filter_by(nama=row["Nama Siswa"]).first()
                    if not cek_nama_siswa:
                        flash("Nama siswa belum ada di database", category="error")
                        return redirect(url_for("data_siswa.data_siswa"))
                    
                    cek_nama_siswa_from_nilai = DatabaseNilaiSiswa.query.filter_by(nama_siswa=row["Nama Siswa"]).first()
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
                        rata_rata = (
                            int(row["pkn"]) +
                            int(row["b_indonesia"]) +
                            int(row["matematika"]) +
                            int(row["ipa"]) +
                            int(row["ips"]) +
                            int(row["b_inggris"]) +
                            int(row["agama"]) +
                            int(row["pjok"]) +
                            int(row["tik"]) +
                            int(row["seni_tari"]) 
                        ) / 10

                        nilai_siswa = DatabaseNilaiSiswa(
                            nama_siswa = row["Nama Siswa"],
                            nisn_siswa = cek_nama_siswa.nisn,
                            agama = row["agama"],
                            pancasila = row["pkn"],
                            indonesia = row["b_indonesia"],
                            matematika = row["matematika"],
                            ipa = row["ipa"],
                            ips = row["ips"],
                            inggris = row["b_inggris"],
                            seni_tari = row["seni_tari"],
                            olahraga = row["pjok"],
                            tik = row["tik"],
                            rata_rata = f"{rata_rata}",
                        )
                        db.session.add(nilai_siswa)
                    
                flash("Success tambah nilai siswa", category="success")
                db.session.commit()

                os.remove(save_path)


        return redirect(url_for("upload_nilai_siswa.upload_nilai_siswa"))
    return render_template("upload-nilai-siswa.html")