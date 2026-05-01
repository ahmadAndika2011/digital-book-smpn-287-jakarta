from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananKunjunganAntarInstansi
from .. import db

auth = Blueprint("layanan_kunjungan_antar_instansi", __name__)

@auth.route("/layanan-kunjungan-antar-instansi", methods=["GET", "POST"])
def layanan_kunjungan_antar_instansi():
    if request.method == "POST":
        tanggal_input = request.form.get("tanggal")
        no_telepon_input = request.form.get("no_telepon")
        nama_input = request.form.get("nama")
        jabatan_input = request.form.get("jabatan")
        keterangan_input = request.form.get("keterangan")

        try:
            valid_tanggal_input = datetime.strptime(tanggal_input, "%Y-%m-%d")
        except:
            valid_tanggal_input = None
        
        if valid_tanggal_input is None:
            flash("Format tanggal tidak valid.", category="error")
        elif len(no_telepon_input) < 10 or len(no_telepon_input) > 12:
            flash("No telepon tidak valid.", category="error")
        elif len(nama_input) < 1:
            flash("Nama tidak valid.", category="error")
        elif len(jabatan_input) < 1:
            flash("Jabatan tidak valid.", category="error")
        else:
            data = DatabaseLayananKunjunganAntarInstansi(
                tanggal=tanggal_input,
                nama=nama_input,
                jabatan=jabatan_input,
                no_telepon=no_telepon_input,
                keterangan=keterangan_input
            )
            db.session.add(data)
            db.session.commit()

    return render_template("layanan-kunjungan-antar-instansi.html")