from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipGuru, DatabaseGuru
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db

auth = Blueprint("tambah_file_arsip", __name__)

@auth.route("/tambah-file-arsip/<int:id>", methods=["GET", "POST"])
@login_required
def tambah_file_arsip(id):
    guru = DatabaseArsipGuru.query.get(id)
    if request.method == "POST":
        file = request.files.get("file_arsip")
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))
            file = filename
        else:
            flash("File Tidak Valid!", category="error")
            return redirect(url_for("tambah_file_arsip.tambah_file_arsip", id=guru.id))

        if guru.list_nama_data is None:
            guru.list_nama_data = []

        guru.list_nama_data.append(file)
        db.session.commit()
        flash("Success Tambah Arsip", category="success")
        return redirect(url_for("detail_arsip_guru.detail_arsip_guru", id=guru.id))

    return render_template("tambah-file-arsip.html", id=guru.id)