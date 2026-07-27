import base64
from email import header
import os
from PIL import Image
from flask import Blueprint, current_app, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananKjpBaru, DatabaseSiswa
from .. import db
from io import BytesIO
from werkzeug.utils import secure_filename

auth = Blueprint("layanan_kjp_baru", __name__)


# ???????????????????????????????????????????????????????????????????????????????????????????????????????????/
@auth.route("/layanan-kjp-baru", methods=["GET", "POST"])
def layanan_kjp_baru():
    if request.method == "POST":
        #? NON GAMBAR
        pemohon_rt_rw = request.form.get("pemohon_rt_rw").strip()
        check_pemohon_rt_rw = pemohon_rt_rw.split("/")
        if len(check_pemohon_rt_rw) != 2:
            flash("Pemohon Rt/Rw tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        pemohon_kode_pos = request.form.get("pemohon_kode_pos").strip()
        if len(pemohon_kode_pos) != 5:
            flash("Pemohon Kode Pos tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        pemohon_telpon = request.form.get("pemohon_telpon").strip()
        if len(pemohon_telpon) > 13 and len(pemohon_telpon) < 10:
            flash("Pemohon No telepon tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        peserta_didik_rt_rw = request.form.get("peserta_didik_rt_rw")
        check_peserta_didik_rt_rw = peserta_didik_rt_rw.split("/")
        if len(check_peserta_didik_rt_rw) != 2:
            flash("Peserta didik Rt/Rw tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        peserta_didik_kode_pos = request.form.get("peserta_didik_kode_pos").strip()
        if len(peserta_didik_kode_pos) != 5:
            flash("Peserta didik Kode Pos tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        sekolah_rt_rw = request.form.get("sekolah_rt_rw")
        check_sekolah_rt_rw = sekolah_rt_rw.split("/")
        if len(check_sekolah_rt_rw) != 2:
            flash("Peserta didik Rt/Rw tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        sekolah_kode_pos = request.form.get("sekolah_kode_pos").strip()
        if len(sekolah_kode_pos) != 5:
            flash("Sekolah Kode Pos tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        pernyataan_nisn = request.form.get("pernyataan_nisn").strip()
        if len(pernyataan_nisn) != 50:
            flash("Pernyataan NISN tidak valid", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        fields = {
        "tanggal_surat" : request.form.get("tanggal_surat"),
        "pemohon_nama" : request.form.get("pemohon_nama"),
        "pemohon_alamat" : request.form.get("pemohon_alamat"),
        "pemohon_kelurahan" : request.form.get("pemohon_kelurahan"),
        "pemohon_kecamatan" : request.form.get("pemohon_kecamatan"),
        "pemohon_kota" : request.form.get("pemohon_kota"),
        "peserta_didik_nama" : request.form.get("peserta_didik_nama"),
        "peserta_didik_tempat_lahir" : request.form.get("peserta_didik_tempat_lahir"),
        "peserta_didik_tanggal_lahir" : request.form.get("peserta_didik_tanggal_lahir"),
        "peserta_didik_jenis_kelamin" : request.form.get("peserta_didik_jenis_kelamin"),
        "peserta_didik_alamat" : request.form.get("peserta_didik_alamat"),
        "peserta_didik_kelurahan" : request.form.get("peserta_didik_kelurahan"),
        "peserta_didik_kecamatan" : request.form.get("peserta_didik_kecamatan"),
        "peserta_didik_kota" : request.form.get("peserta_didik_kota"),
        "sekolah_nama" : request.form.get("sekolah_nama"),
        "sekolah_alamat" : request.form.get("sekolah_alamat"),
        "sekolah_kelurahan" : request.form.get("sekolah_kelurahan"),
        "sekolah_kecamatan" : request.form.get("sekolah_kecamatan"),
        "sekolah_kota" : request.form.get("sekolah_kota"),
        "ttd_nama_lengkap" : request.form.get("ttd_nama_lengkap"),
        "pernyataan_nama_peserta_didik" : request.form.get("pernyataan_nama_peserta_didik"),
        "pernyataan_kelas" : request.form.get("pernyataan_kelas"),
        "pernyataan_sekolah" : request.form.get("pernyataan_sekolah"),
        "pernyataan_nama_orang_tua" : request.form.get("pernyataan_nama_orang_tua"),
        "pernyataan_alamat" : request.form.get("pernyataan_alamat"),
        }
        for name_field, value in fields.items():
            if not value:
                flash(f"{name_field} wajib diisi", category="error")
                return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        #? GAMBAR
        lampiran_kk = request.files.get("lampiran_kk")
        lampiran_ktp = request.files.get("lampiran_ktp")
        ttd_tanda_tangan = request.files.get("ttd_tanda_tangan")
        pernyataan_ttd_orang_tua = request.files.get("pernyataan_ttd_orang_tua")
        pernyataan_ttd_penerima = request.files.get("pernyataan_ttd_penerima")
        if lampiran_kk:
            filename = secure_filename(lampiran_kk.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            lampiran_kk.save(os.path.join("website/static/uploads", filename))
            lampiran_kk = filename
        else:
            flash("KK belum di masukkan", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))
        
        if lampiran_ktp:
            filename = secure_filename(lampiran_ktp.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            lampiran_ktp.save(os.path.join("website/static/uploads", filename))
            lampiran_ktp = filename
        else:
            flash("KJP belum di masukkan", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        if ttd_tanda_tangan:
            filename = secure_filename(ttd_tanda_tangan.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            ttd_tanda_tangan.save(os.path.join("website/static/uploads", filename))
            ttd_tanda_tangan = filename
        else:
            flash("TTD Pemohon belum di masukkan", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        if pernyataan_ttd_orang_tua:
            filename = secure_filename(pernyataan_ttd_orang_tua.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            pernyataan_ttd_orang_tua.save(os.path.join("website/static/uploads", filename))
            pernyataan_ttd_orang_tua = filename
        else:
            flash("TTD orang tua belum di masukkan", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        if pernyataan_ttd_penerima:
            filename = secure_filename(pernyataan_ttd_penerima.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            pernyataan_ttd_penerima.save(os.path.join("website/static/uploads", filename))
            pernyataan_ttd_penerima = filename
        else:
            flash("TTD penerima belum di masukkan", category="error")
            return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))

        data_kjp = DatabaseLayananKjpBaru(
            tanggal_surat = fields["tanggal_surat"],
            pemohon_nama = fields["pemohon_nama"],
            pemohon_alamat = fields["pemohon_alamat"],
            pemohon_rt_rw = pemohon_rt_rw,
            pemohon_kelurahan = fields["pemohon_kelurahan"],
            pemohon_kecamatan = fields["pemohon_kecamatan"],
            pemohon_kota = fields["pemohon_kota"],
            pemohon_kode_pos = pemohon_kode_pos,
            pemohon_telpon = pemohon_telpon,
            peserta_didik_nama = fields["peserta_didik_nama"],
            peserta_didik_tempat_lahir = fields["peserta_didik_tempat_lahir"],
            peserta_didik_tanggal_lahir = fields["peserta_didik_tanggal_lahir"],
            peserta_didik_jenis_kelamin = fields["peserta_didik_jenis_kelamin"],
            peserta_didik_alamat = fields["peserta_didik_alamat"],
            peserta_didik_rt_rw = peserta_didik_rt_rw,
            peserta_didik_kelurahan = fields["peserta_didik_kelurahan"],
            peserta_didik_kecamatan = fields["peserta_didik_kecamatan"],
            peserta_didik_kota = fields["peserta_didik_kota"],
            peserta_didik_kode_pos = peserta_didik_kode_pos,
            sekolah_nama = fields["sekolah_nama"],
            sekolah_alamat = fields["sekolah_alamat"],
            sekolah_rt_rw = sekolah_rt_rw,
            sekolah_kelurahan = fields["sekolah_kelurahan"],
            sekolah_kecamatan = fields["sekolah_kecamatan"],
            sekolah_kota = fields["sekolah_kota"],
            sekolah_kode_pos = sekolah_kode_pos,
            lampiran_kk = lampiran_kk,
            lampiran_ktp = lampiran_ktp,
            ttd_nama_lengkap = fields["ttd_nama_lengkap"],
            ttd_tanda_tangan = ttd_tanda_tangan,
            pernyataan_nama_peserta_didik = fields["pernyataan_nama_peserta_didik"],
            pernyataan_nisn = pernyataan_nisn,
            pernyataan_kelas = fields["pernyataan_kelas"],
            pernyataan_sekolah = fields["pernyataan_sekolah"],
            pernyataan_nama_orang_tua = fields["pernyataan_nama_orang_tua"],
            pernyataan_alamat = fields["pernyataan_alamat"],
            pernyataan_ttd_orang_tua = pernyataan_ttd_orang_tua,
            pernyataan_ttd_penerima = pernyataan_ttd_penerima
        )
        db.session.add(data_kjp)
        db.session.commit()

        flash("Success Upload form KJP, silahkan tunggu informasi lebih lanjut dari pihak sekolah.", category="success")
        return redirect(url_for("layanan_kjp_baru.layanan_kjp_baru"))


    return render_template("layanan-kjp-baru.html")
