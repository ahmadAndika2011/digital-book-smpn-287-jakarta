from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from werkzeug.utils import secure_filename
from .. import db
from ..models import DatabaseGuru
import xlrd

auth = Blueprint("upload_data_guru", __name__)

ALLOWED_FORMAT = ["xlsx", "xls"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

@auth.route("/upload-data-guru", methods=["GET", "POST"])
def upload_data_guru():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                filename = secure_filename(file.filename)
                df_guru = pd.read_excel(save_path, dtype={"nip": str, "nrk": str})
                df_guru = df_guru.fillna("")

                list_error_update = []
                
                for index, row in df_guru.iterrows():
                    db.session.rollback()
                    existing = DatabaseGuru.query.filter(
                        DatabaseGuru.nip == row["nip"],
                        DatabaseGuru.nrk == row["nrk"],
                    ).first()

                    if existing:
                        list_error_update.append("NIP dan NRK")
                        continue

                    data_guru = DatabaseGuru(
                        image="",
                        name=row["nama"],
                        mapel=row["mapel"],
                        nip=row["nip"],
                        nrk=row["nrk"],
                        status=row["status"],
                        jabatan=row["jabatan"],
                        tahun_masuk=row["tahun_masuk"]
                    )
                    db.session.add(data_guru)
                    db.session.commit()
                os.remove(save_path)
                for e in list_error_update:
                    flash(e, category="error")
                
                return redirect(url_for("views.home"))
    return render_template("upload_file_guru.html")