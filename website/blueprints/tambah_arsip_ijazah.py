from fileinput import filename

from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipIjazah
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db

auth = Blueprint("tambah_arsip_ijazah", __name__)

UPLOAD_FOLDER = os.path.join('website', 'static', 'uploads')  # sesuaikan path
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', "csv", "xlsx", "xls"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/tambah-arsip-ijazah/<tahun>", methods=["GET", "POST"])
@login_required
def tambah_arsip_ijazah(tahun):
    if request.method == "POST":
        nisn = request.form.get("nisn")
        arsip = request.files.get("arsip")
        if arsip:
            nama_arsip = secure_filename(arsip.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            arsip.save(os.path.join(upload_path, nama_arsip))
        else:
            flash("File Tidak Valid!", category="error")
            return redirect(url_for("tambah_arsip_ijazah.tambah_arsip_ijazah", tahun=tahun))

        new_arsip = DatabaseArsipIjazah(
            nisn=nisn,
            nama_arsip=nama_arsip,
            tahun=tahun
        )
        db.session.add(new_arsip)

        db.session.commit()
        flash("success tambah arsip Ijazah", category="success")
        return redirect(url_for("tambah_arsip_ijazah.tambah_arsip_ijazah", tahun=tahun))
        
    return render_template("tambah-arsip-ijazah.html", tahun=tahun)