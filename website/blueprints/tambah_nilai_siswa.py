from flask import Blueprint, render_template,  flash, redirect, url_for, request
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from ..models import DatabaseSiswa, DatabaseNilaiSiswa
from datetime import datetime
from .. import db

auth = Blueprint("tambah_nilai_siswa", __name__)

@auth.route("tambah-nilai-siswa", methods=["GET", "POST"])
def tambah_nilai_siswa():
    if request.method == "POST":
        name = request.form.get("name", "").strip().upper()
        nisn = request.form.get("nisn", "")
        n_agama = request.form.get("n_agama", "")
        n_pancasila = request.form.get("n_pancasila", "")
        n_indonesia = request.form.get("n_indonesia", "")
        n_matematika = request.form.get("n_matematika", "")
        n_ipa = request.form.get("n_ipa", "")
        n_ips = request.form.get("n_ips", "")
        n_inggris = request.form.get("n_inggris", "")
        n_seni_tari = request.form.get("n_seni_tari", "")
        n_olahraga = request.form.get("n_olahraga", "")
        n_tik = request.form.get("n_tik", "")

        cek_nama_siswa = DatabaseSiswa.query.filter_by(nama=name).first()
        cek_nisn_siswa = DatabaseSiswa.query.filter_by(nisn=nisn).first()
        cek_nama_siswa_from_nilai = DatabaseNilaiSiswa.query.filter_by(nama_siswa=name).first()

        if not cek_nama_siswa_from_nilai:
            flash("Data ini sudah ada di database", category="error")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
        elif not cek_nama_siswa:
            flash("Nama siswa belum ada di database", category="error")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
        elif len(nisn) != 10:
            flash("NISN harus terdiri dari 10 digit", category="error")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
        elif not cek_nisn_siswa:
            flash("NISN siswa belum ada di database", category="error")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
        elif(
            name and
            n_agama and
            n_pancasila and
            n_indonesia and
            n_matematika and
            n_ipa and
            n_ips and
            n_inggris and
            n_seni_tari and
            n_olahraga and
            n_tik and
            cek_nama_siswa and
            cek_nisn_siswa
        ):
            rata_rata = (
                int(n_agama) + 
                int(n_pancasila) + 
                int(n_indonesia) + 
                int(n_matematika) + 
                int(n_ipa) + 
                int(n_ips) + 
                int(n_inggris) + 
                int(n_seni_tari) + 
                int(n_olahraga)  +
                int(n_tik)  
            ) / 10

            nilai_siswa = DatabaseNilaiSiswa(
                nama_siswa = name,
                nisn_siswa = nisn,
                agama = n_agama,
                pancasila = n_pancasila,
                indonesia = n_indonesia,
                matematika = n_matematika,
                ipa = n_ipa,
                ips = n_ips,
                inggris = n_inggris,
                seni_tari = n_seni_tari,
                olahraga = n_olahraga,
                tik = n_tik,
                rata_rata = f"{rata_rata}",
            )
            db.session.add(nilai_siswa)
            db.session.commit()
            flash("Success tambah nilai siswa", category="success")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
        else:
            flash("Data Tidak lengkap\nMohon lengkapi nilai", category="error")
            return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))

        return redirect(url_for("tambah_nilai_siswa.tambah_nilai_siswa"))
    return render_template("tambah-nilai-siswa.html")