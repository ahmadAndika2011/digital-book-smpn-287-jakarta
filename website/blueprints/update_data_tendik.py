from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..models import DatabaseTendik
from .. import db


auth = Blueprint("update_data_tendik", __name__)

@auth.route("/update-data-tendik/<int:id>", methods=["GET", "POST"])
@login_required
def update_data_tendik(id):
    guru = DatabaseTendik.query.get(id)
    status = ["PNS", "PPPK", "KKI"]

    if request.method == "POST":
        gambar_file = request.files.get("gambar")
        if gambar_file and gambar_file.filename:
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join(upload_path, filename))
            gambar_file_new = filename
        else:
            gambar_file_new = None

        name_new = request.form.get("name")
        bagian_new = request.form.get("bagian")
        nip_new = request.form.get("nip")
        nrk_new = request.form.get("nrk")
        status_new = request.form.get("status")
        jabatan_new = request.form.get("jabatan")
        tahun_masuk_new = request.form.get("tahun_masuk")

        if gambar_file != None:
            guru.image = gambar_file_new
        
        if name_new:
            guru.name = name_new

        if bagian_new:
            guru.bagian = bagian_new.upper()

        if len(nip_new) == 18:
            guru.nip = nip_new

        if len(nrk_new) == 6:
            guru.nrk = nrk_new

        if status_new:
            guru.status = status_new.upper()

        if jabatan_new:
            guru.jabatan = jabatan_new.upper()

        if tahun_masuk_new:
            guru.tahun_masuk = tahun_masuk_new

        flash("Success Update data Tendik.", category="success")
        db.session.commit()
        return redirect(url_for("detail_tendik.detail_tendik", id=guru.id))

    return render_template("update-data-tendik.html", user=current_user, guru=guru, status=status)