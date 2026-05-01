from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananMutasi
from .. import db

auth = Blueprint("layanan_mutasi", __name__)

@auth.route("/layanan-mutasi", methods=["GET", "POST"])
def layanan_mutasi():
    if request.method == "POST":
        jenis_mutasi_input = request.form.get("jenis_mutasi")
        tanggal_input = request.form.get("tanggal")
        no_telepon_input = request.form.get("no_telepon")
        nama_input = request.form.get("nama")
        sekolah_asal_input = request.form.get("sekolah_asal")
        keterangan_input = request.form.get("keterangan")

        try: 
            valid_tanggal_input = datetime.strptime(tanggal_input, "%Y-%m-%d")
        except:
            valid_tanggal_input = None
        if valid_tanggal_input == None:
            flash("Format Tanggal tidak valid.", category="error")
            return redirect(url_for("layanan_mutasi.layanan_mutasi"))
        elif jenis_mutasi_input == "":
            flash("Pilih jenis Mutasi.", category="error")
            return redirect(url_for("layanan_mutasi.layanan_mutasi"))
        elif len(no_telepon_input) > 12 or len(no_telepon_input) < 10:
            flash("No Telpon Tidak valid.", category="error")
            return redirect(url_for("layanan_mutasi.layanan_mutasi"))
        elif len(nama_input) < 1:
            flash("Nama siswa harus di isi.", category="error")
            return redirect(url_for("layanan_mutasi.layanan_mutasi"))
        elif len(sekolah_asal_input) < 1:
            flash("Asal Sekolah siswa harus di isi.", category="error")
            return redirect(url_for("layanan_mutasi.layanan_mutasi"))
        else:
            data = DatabaseLayananMutasi(
                tanggal=tanggal_input,
                nama=nama_input,
                sekolah_asal=sekolah_asal_input,
                no_telepon=no_telepon_input,
                keterangan=keterangan_input,
                jenis_mutasi=jenis_mutasi_input
            )
            db.session.add(data)
            db.session.commit()
            flash("Berhasil Tambah ke antrian.", category="success")
            return redirect(url_for("views.home"))

    return render_template("layanan-mutasi.html")
