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
        error = DatabaseArsipGuru.query.filter_by(nrk=nrk).first()

        if error:
            flash("Data Sudah ada di database Arsip Guru", category="error")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))

        if not nama or not nrk:
            flash("Nama dan NRK wajib diisi", category="error")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
        if len(nama) < 1:
            flash("Nama wajib diisi", category="error")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
        if len(nrk) != 6:
            flash("NRK harus sama dengan 6", category="error")
            return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))

        new_arsip = DatabaseArsipGuru(
            nama=nama,
            nrk=nrk,
            list_nama_data=[]
        )
        db.session.add(new_arsip)

        db.session.commit()
        flash("success tambah arsip guru", category="success")
        return redirect(url_for("tambah_arsip_guru.tambah_arsip_guru"))
        
    return render_template("tambah-arsip-guru.html")