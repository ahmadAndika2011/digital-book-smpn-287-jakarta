from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananKjp
from .. import db

auth = Blueprint("layanan_kjp", __name__)


@auth.route("/layanan-kjp", methods=["GET", "POST"])
def layanan_kjp():
    if request.method == "POST":
        # data siswa
        nik_murid = request.form.get("nik_murid")
        nama_murid = request.form.get("nama_murid")
        jenis_kelamin_murid = request.form.get("jenis_kelamin_murid")
        agama_murid = request.form.get("agama_murid")
        tempat_lahir_murid = request.form.get("tempat_lahir_murid")
        tanggal_lahir_murid = request.form.get("tanggal_lahir_murid")
        nama_ibu_kandung_murid = request.form.get("nama_ibu_kandung_murid")
        kelas = request.form.get("kelas")
        nisn_murid = request.form.get("nisn_murid")
        pendidikan = request.form.get("pendidikan")
        no_hp_murid = request.form.get("no_hp_murid")
        no_telepon = request.form.get("no_telepon")
        masa_berlaku_identitas = request.form.get("masa_berlaku_identitas")
        untuk_disabilitas = request.form.get("untuk_disabilitas")

        no_kartu_keluarga = request.form.get("no_kartu_keluarga")
        tipe_alamat = request.form.get("tipe_alamat")
        status_tempat_tinggal = request.form.get("status_tempat_tinggal")
        alamat_surat = request.form.get("alamat_surat")

        # cek
        if (
            len(nik_murid) != 16
            or not nama_murid
            or not jenis_kelamin_murid
            or not agama_murid
            or not tempat_lahir_murid
            or not tanggal_lahir_murid
            or not nama_ibu_kandung_murid
            or not kelas
            or not nisn_murid
            or not pendidikan
            or (len(no_hp_murid) < 10 or len(no_hp_murid) > 12)
            or (len(no_telepon) < 10 or len(no_telepon) > 12)
            or len(no_kartu_keluarga) != 16
            or not tipe_alamat
            or not status_tempat_tinggal
            or not alamat_surat   # ✅ ini yang benar
        ):
            flash("Data tidak valid.\nSilahkan cek kembali data anda", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        else:
            if not masa_berlaku_identitas:
                data_kjp = DatabaseLayananKjp(
                    nik_murid = nik_murid,
                    no_kartu_keluarga = no_kartu_keluarga,
                    nama_murid = nama_murid,
                    jenis_kelamin_murid = jenis_kelamin_murid,
                    tempat_lahir_murid = tempat_lahir_murid,
                    tanggal_lahir_murid = tanggal_lahir_murid,
                    nama_ibu_kandung_murid = nama_ibu_kandung_murid,
                    kelas = kelas,
                    nisn_murid = nisn_murid,
                    masa_berlaku_identitas = "Seumur Hidup",
                    no_hp_murid = no_hp_murid,
                    no_telepon = no_telepon,
                    alamat_surat = alamat_surat,
                    tipe_alamat = tipe_alamat,
                    status_tempat_tinggal = status_tempat_tinggal,
                    agama_murid = agama_murid,
                    pendidikan = pendidikan,
                    untuk_disabilitas = untuk_disabilitas,
                )
                db.session.add(data_kjp)
            else:
                data_kjp = DatabaseLayananKjp(
                    nik_murid = nik_murid,
                    no_kartu_keluarga = no_kartu_keluarga,
                    nama_murid = nama_murid,
                    jenis_kelamin_murid = jenis_kelamin_murid,
                    tempat_lahir_murid = tempat_lahir_murid,
                    tanggal_lahir_murid = tanggal_lahir_murid,
                    nama_ibu_kandung_murid = nama_ibu_kandung_murid,
                    kelas = kelas,
                    nisn_murid = nisn_murid,
                    masa_berlaku_identitas = masa_berlaku_identitas,
                    no_hp_murid = no_hp_murid,
                    no_telepon = no_telepon,
                    alamat_surat = alamat_surat,
                    tipe_alamat = tipe_alamat,
                    status_tempat_tinggal = status_tempat_tinggal,
                    agama_murid = agama_murid,
                    pendidikan = pendidikan,
                    untuk_disabilitas = untuk_disabilitas,
                )
                db.session.add(data_kjp)
            db.session.commit()
            flash("Success Menambahkan data.", category="success")
        return redirect(url_for("views.home"))
    return render_template("layanan-kjp.html")
