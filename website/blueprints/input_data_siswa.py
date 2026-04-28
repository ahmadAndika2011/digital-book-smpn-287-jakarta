from flask import Blueprint, render_template,  flash, redirect, url_for, request
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from ..models import DatabaseSiswa, NilaiSiswa
from datetime import datetime
from .. import db

auth = Blueprint("input_data_siswa", __name__)

@auth.route("/input", methods=["GET", "POST"])
@login_required
def input():
    if request.method == "POST":
        # input data Murid
        gambar_file = request.files.get("gambar")
        if gambar_file:
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            gambar_input = filename
        else:
            gambar_input = None

        name_input = request.form.get("name")
        nisn_input = request.form.get("nisn")
        nis_input = request.form.get("nis")
        tanggal_lahir_input = request.form.get("tanggal_lahir")
        tempat_lahir_input = request.form.get("tempat_lahir")
        agama_input = request.form.get("agama")
        alamat_input = request.form.get("alamat")
        rt_input = request.form.get("rt")
        rw_input = request.form.get("rw")
        kelurahan_input = request.form.get("kelurahan")
        kecamatan_input = request.form.get("kecamatan")
        sekolah_asal_input = request.form.get("sekolah_asal")
        lulus_input = request.form.get("lulus")
        check_duplicate_nisn = DatabaseSiswa.query.filter_by(
            nisn=nisn_input).first()
        check_duplicate_nis = DatabaseSiswa.query.filter_by(
            nis=nis_input).first()
        # input Nilai Murid
        n_agama_input = request.form.get("n_agama")
        n_pancasila_input = request.form.get("n_pancasila")
        n_indonesia_input = request.form.get("n_indonesia")
        n_matematika_input = request.form.get("n_matematika")
        n_ipa_input = request.form.get("n_ipa")
        n_ips_input = request.form.get("n_ips")
        n_inggris_input = request.form.get("n_inggris")
        n_seni_budaya_input = request.form.get("n_seni_budaya")
        n_olahraga_input = request.form.get("n_olahraga")
        n_prakarya_input = request.form.get("n_prakarya")

        try:
            valid_date = datetime.strptime(tanggal_lahir_input, "%Y-%m-%d")
        except Exception as e:
            valid_date = None

        if check_duplicate_nisn:
            flash("NISN sudah ada.", category="error")
        elif check_duplicate_nis:
            flash("NIS sudah ada.", category="error")
        elif len(nisn_input) != 10:
            flash("NISN harus 10 digit.", category="error")
        elif len(nis_input) != 4:
            flash("NIS harus 4 digit.", category="error")
        elif not valid_date:
            flash("Tanggal lahir tidak valid.", category="error")
        else:
            data_siswa = DatabaseSiswa(
                image=gambar_input,
                nama=name_input,
                nisn=nisn_input,
                nis=nis_input,
                tanggal_lahir=tanggal_lahir_input,
                tempat_lahir=tempat_lahir_input,
                agama=agama_input,
                alamat=alamat_input,
                rt=rt_input,
                rw=rw_input,
                kelurahan=kelurahan_input,
                kecamatan=kecamatan_input,
                sekolah_asal=sekolah_asal_input,
                lulus=lulus_input.title()
            )
            nilai_siswa = NilaiSiswa(
                nisn=nisn_input,
                agama=n_agama_input,
                pancasila=n_pancasila_input,
                indonesia=n_indonesia_input,
                matematika=n_matematika_input,
                ipa=n_ipa_input,
                ips=n_ips_input,
                inggris=n_inggris_input,
                seni_budaya=n_seni_budaya_input,
                olahraga=n_olahraga_input,
                prakarya=n_prakarya_input
            )
            db.session.add(data_siswa)
            db.session.add(nilai_siswa)
            db.session.commit()
            flash("Berhasil tambah data.", category="success")

    return render_template("input.html", user=current_user)
