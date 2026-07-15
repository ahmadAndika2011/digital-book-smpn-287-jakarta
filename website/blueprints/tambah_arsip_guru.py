from fileinput import filename

from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipGuru, DatabaseGuru
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db

auth = Blueprint("tambah_arsip_guru", __name__)

UPLOAD_FOLDER = os.path.join('website', 'static', 'uploads')  # sesuaikan path
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', "csv", "xlsx", "xls"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/tambah-arsip-guru", methods=["GET", "POST"])
@login_required
def tambah_arsip_guru():
    if request.method == "POST":
        nama = request.form.get("nama")
        nrk = request.form.get("nrk")
        file = request.files.get("nama_data")

        if not nama or not nrk:
            flash("Nama dan NRK wajib diisi")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
        if len(nama) < 1:
            flash("Nama wajib diisi")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
        if len(nrk) != 6:
            flash("NRK harus sama dengan 6")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))

        if not file or file.filename == '' or not allowed_file(file.filename):
            flash("Silakan pilih file arsip yang valid")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))

        filename = secure_filename(file.filename)

        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        file.save(os.path.join(upload_path, filename))

        new_arsip = DatabaseArsipGuru(
            nama=nama,
            nrk=nrk,
            list_nama_data=filename
        )
        db.session.add(new_arsip)

        db.session.commit()
        flash("success tambah arsip guru")
        return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
    return render_template("tambah-arsip-guru.html")