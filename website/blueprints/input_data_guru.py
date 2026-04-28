
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..models import DataGuru
from .. import db


auth = Blueprint("input_data_guru", __name__)

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
            return redirect(url_for("input_data_guru.tambah_data_guru"))
        else:
            flash("Jika NIP tidak lengkap maka bisa dikosongkan untuk mencegah kesalahan", category="error")
    return render_template("tambah-data-guru.html", user=current_user)