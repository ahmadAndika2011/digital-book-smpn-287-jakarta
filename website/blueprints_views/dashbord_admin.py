from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_required
from pandas import read_sql_query

from website.views import role_required
from ..models import DatabaseLayananPpdb, DatabaseLayananMutasi, DatabaseLayananPip, DatabaseLayananKjp, DatabaseLayananAdministrasiSekolah, DatabaseLayananKunjunganAntarInstansi
import pandas as pd
from .. import db
import io
import os
import zipfile
from datetime import datetime
from .fill_kjp_pdf import fill_kjp_pdf

PDF_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "static", "uploads",
    "kjp_format.pdf"
)

views = Blueprint("dashbord_admin", __name__)


@views.route("/dashbord-admin")
@login_required
@role_required("superadmin", "layanan")
def dashbord_admin():
    data_layanan_ppdb = DatabaseLayananPpdb.query.all()
    data_layanan_mutasi = DatabaseLayananMutasi.query.all()
    data_layanan_pip = DatabaseLayananPip.query.all()
    data_layanan_kjp = DatabaseLayananKjp.query.all()
    data_layanan_administrasi_sekolah = DatabaseLayananAdministrasiSekolah.query.all()
    data_layanan_kunjungan_antar_instansi = DatabaseLayananKunjunganAntarInstansi.query.all()
    return render_template("dashbord-admin.html",
                           user=current_user,
                           data_layanan_ppdb=data_layanan_ppdb,
                           data_layanan_mutasi=data_layanan_mutasi,
                           data_layanan_pip=data_layanan_pip,
                           data_layanan_kjp=data_layanan_kjp,
                           data_layanan_administrasi_sekolah=data_layanan_administrasi_sekolah,
                           data_layanan_kunjungan_antar_instansi=data_layanan_kunjungan_antar_instansi
                           )


@views.route("/download-data-kjp", methods=["POST"])
def download_data_kjp():
    if request.method == "POST":
        # Ambil semua data siswa KJP dari database
        semua_siswa = DatabaseLayananKjp.query.all()

        # Buat file ZIP di memori (RAM), isinya 1 PDF per siswa
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for siswa in semua_siswa:
                # Ubah objek database menjadi dictionary
                siswa_dict = {
                    "id":         siswa.id,
                    # "tanggal":    str(siswa.tanggal) if siswa.tanggal else "",
                    "nama_murid":       siswa.nama_murid or "",
                    "tempat_lahir_murid":       siswa.tempat_lahir_murid or "",
                    "nik_murid":       siswa.nik_murid or "",
                    "no_kartu_keluarga": siswa.no_kartu_keluarga or "",
                    "jenis_kelamin_murid": siswa.jenis_kelamin_murid or "",
                    "tanggal_lahir_murid": siswa.tanggal_lahir_murid or "",
                    "nama_ibu_kandung_murid": siswa.nama_ibu_kandung_murid or "",
                    "kelas": siswa.kelas or "",
                    "nisn_murid": siswa.nisn_murid or "",
                    "masa_berlaku_identitas": siswa.masa_berlaku_identitas or "",
                    "no_hp_murid": siswa.no_hp_murid or "",
                    "no_telepon": siswa.no_telepon or "",
                    "alamat_surat": siswa.alamat_surat or "",
                    "tipe_alamat": siswa.tipe_alamat or "",
                    "status_tempat_tinggal": siswa.status_tempat_tinggal or "",
                    "agama_murid": siswa.agama_murid or "",
                    "untuk_disabilitas": siswa.untuk_disabilitas or "",
                    "npwp_murid": siswa.npwp_murid or "",
                    "alamat_murid": siswa.alamat_murid or "",
                    "rt_murid": siswa.rt_murid or "",
                    "rw_murid": siswa.rw_murid or "",
                    "provinsi_murid": siswa.provinsi_murid or "",
                    "kota_murid": siswa.kota_murid or "",
                    "kecamatan_murid": siswa.kecamatan_murid or "",
                    "kelurahan_murid": siswa.kelurahan_murid or "",
                    "kode_pos_murid": siswa.kode_pos_murid or "",
                    "nama_wali": siswa.nama_wali or "",
                    "no_ktp_wali": siswa.no_ktp_wali or "",
                    "masa_berlaku_ktp_wali": siswa.masa_berlaku_ktp_wali or "",
                    "npwp_wali": siswa.npwp_wali or "",
                    "kartu_keluarga_wali": siswa.kartu_keluarga_wali or "",
                    "tempat_lahir_wali": siswa.tempat_lahir_wali or "",
                    "tanggal_lahir_wali": siswa.tanggal_lahir_wali or "",
                    "jenis_kelamin_wali": siswa.jenis_kelamin_wali or "",
                    "agama_wali": siswa.agama_wali or "",
                    "nama_ibu_kandung_wali": siswa.nama_ibu_kandung_wali or "",
                    "pekerjaan_wali": siswa.pekerjaan_wali or "",
                    "status_pernikahan_wali": siswa.status_pernikahan_wali or "",
                    "pendidikan_wali": siswa.pendidikan_wali or "",
                    "jabatan_wali": siswa.jabatan_wali or "",
                    "alamat_wali": siswa.alamat_wali or "",
                }

                # Isi formulir PDF dengan data siswa
                pdf_bytes = fill_kjp_pdf(
                    siswa_dict, template_path=PDF_TEMPLATE_PATH)

                # Simpan PDF ke dalam ZIP dengan nama file berdasarkan nama siswa
                nama_file = (
                    siswa.nama_murid or f"siswa_{siswa.id}").replace(" ", "_")
                zf.writestr(
                    f"KJP_{nama_file}_{datetime.now().year}.pdf", pdf_bytes)

        zip_buffer.seek(0)

        # Kirim file ZIP ke browser untuk didownload
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"KJP_PLUS_{datetime.now().year}.zip"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))
