from fileinput import filename

from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime

from flask_wtf import file
from werkzeug.utils import secure_filename
from ..models import DatabaseLayananPip
from .. import db
import os

auth = Blueprint("layanan_pip", __name__)

@auth.route("/layanan-pip", methods=["GET", "POST"])
def layanan_pip():
    if request.method == "POST":
        tanggal_input = request.form.get("tanggal")
        no_telepon_input = request.form.get("no_telepon")
        nama_input = request.form.get("nama")
        keterangan_input = request.form.get("keterangan")

        gambar_1_file = request.files.get("buku_depan")
        if gambar_1_file and gambar_1_file.filename != "":
            filename = secure_filename(gambar_1_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_1_file.save(os.path.join(upload_path, filename))
            gambar_1_input = filename
        else:
            gambar_1_input = None

        gambar_2_file = request.files.get("buku_mutasi")
        if gambar_2_file and gambar_2_file.filename != "":
            filename = secure_filename(gambar_2_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_2_file.save(os.path.join(upload_path, filename))
            gambar_2_input = filename
        else:
            gambar_2_input = None

        try:
            valid_tanggal_input = datetime.strptime(tanggal_input, "%Y-%m-%d")
        except:
            valid_tanggal_input = None
        if valid_tanggal_input == None:
            flash("Format Tanggal tidak valid.", category="error")
            return redirect(url_for("layanan_pip.layanan_pip"))
        elif len(no_telepon_input) > 12 or len(no_telepon_input) < 10:
            flash("No Telpon Tidak valid.", category="error")
            return redirect(url_for("layanan_pip.layanan_pip"))
        elif len(nama_input) < 1:
            flash("Nama calon siswa harus di isi.", category="error")
            return redirect(url_for("layanan_pip.layanan_pip"))
        else:
            data = DatabaseLayananPip(
                tanggal=tanggal_input,
                nama=nama_input,
                no_telepon=no_telepon_input,
                keterangan=keterangan_input,
                image_1 = gambar_1_input,
                image_2 = gambar_2_input,
            )
            db.session.add(data)
            db.session.commit()
            flash("Berhasil Tambah ke antrian.", category="success")
            return redirect(url_for("views.home"))
        
    return render_template("layanan-pip.html")
