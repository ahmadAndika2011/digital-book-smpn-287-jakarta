from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananPpdb
from .. import db

auth = Blueprint("layanan_ppdb", __name__)

@auth.route("/layanan-ppdb", methods=["GET", "POST"])
def layanan_ppdb():
    if request.method == "POST":
        tanggal_input = request.form.get("tanggal")
        no_telepon_input = request.form.get("no_telepon")
        nama_calon_siswa_input = request.form.get("nama_calon_siswa")
        keterangan_input = request.form.get("keterangan")

        try:
            valid_tanggal_input = datetime.strptime(tanggal_input, "%Y-%m-%d")
        except:
            valid_tanggal_input = None
        
        if valid_tanggal_input == None:
            flash("Format Tanggal tidak valid.", category="error")
            return redirect(url_for("layanan_ppdb.layanan_ppdb"))
        elif len(no_telepon_input) > 12 or len(no_telepon_input) < 10:
            flash("No Telpon Tidak valid.", category="error")
            return redirect(url_for("layanan_ppdb.layanan_ppdb"))
        elif len(nama_calon_siswa_input) < 1:
            flash("Nama calon siswa harus di isi.", category="error")
            return redirect(url_for("layanan_ppdb.layanan_ppdb"))
        else:
            data = DatabaseLayananPpdb(
                tanggal=tanggal_input,
                nama_calon_siswa=nama_calon_siswa_input,
                no_telepon=no_telepon_input,
                keterangan=keterangan_input
            )
            db.session.add(data)
            db.session.commit()
            flash("Berhasil Tambah ke antrian.", category="success")
            return redirect(url_for("views.home"))

    return render_template("layanan-ppdb.html")
