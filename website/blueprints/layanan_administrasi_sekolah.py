from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananAdministrasiSekolah
from .. import db

auth = Blueprint("layanan_administrasi_sekolah", __name__)

@auth.route("layanan-administrasi-sekolah", methods=["GET", "POST"])
def layanan_administrasi_sekolah():
    if request.method == "POST":
        tanggal_pengajuan_input = request.form.get("tanggal_pengajuan")
        no_telepon_input = request.form.get("no_telepon")
        nama_input = request.form.get("nama")
        tanggal_pengambilan_input = request.form.get("tanggal_pengambilan")
        keterangan_input = request.form.get("keterangan")

        try:
            valid_tanggal_pengajuan = datetime.strptime(tanggal_pengajuan_input, "%Y-%m-%d")
        except:
            valid_tanggal_pengajuan = None

        try:
            valid_tanggal_pengambilan = datetime.strptime(tanggal_pengambilan_input, "%Y-%m-%d")
        except:
            valid_tanggal_pengambilan = None

        if valid_tanggal_pengajuan is None or valid_tanggal_pengambilan is None:
            flash("Format tanggal tidak valid.", category="error")
        elif len(no_telepon_input) < 10 or len(no_telepon_input) > 12:
            flash("No telepon tidak valid.", category="error")
        elif len(nama_input) < 1:
            flash("Nama tidak valid.", category="error")
        else:
            data = DatabaseLayananAdministrasiSekolah(
                tanggal_pengajuan=tanggal_pengajuan_input,
                nama=nama_input,
                tanggal_pengambilan=tanggal_pengambilan_input, 
                no_telepon=no_telepon_input,
                keterangan=keterangan_input
            )
            db.session.add(data)
            db.session.commit()
            flash("Success Tambah Keantrian")
            return redirect(url_for("views.home"))

    return render_template("layanan-administrasi-sekolah.html")