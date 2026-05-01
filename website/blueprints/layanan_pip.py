from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananPip
from .. import db

auth = Blueprint("layanan_pip", __name__)

@auth.route("/layanan-pip", methods=["GET", "POST"])
def layanan_pip():
    if request.method == "POST":
        tanggal_input = request.form.get("tanggal")
        no_telepon_input = request.form.get("no_telepon")
        nama_input = request.form.get("nama")
        keterangan_input = request.form.get("keterangan")

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
                keterangan=keterangan_input
            )
            db.session.add(data)
            db.session.commit()
            flash("Berhasil Tambah ke antrian.", category="success")
            return redirect(url_for("views.home"))
        
    return render_template("layanan-pip.html")
