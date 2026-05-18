from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_required
from pandas import read_sql_query
from ..models import DatabaseLayananPpdb, DatabaseLayananMutasi, DatabaseLayananPip, DatabaseLayananKjp, DatabaseLayananAdministrasiSekolah, DatabaseLayananKunjunganAntarInstansi
import pandas as pd
from .. import db
import io
import os
import zipfile
from datetime import datetime
from .fill_kjp_pdf import fill_kjp_pdf_berita_acara, fill_kjp_pdf, fill_kjp_pdf_surat_pernyataan, fill_kjp_pdf_permohonan
import pandas as pd

PDF_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "static", "uploads",
    "kjp_format.pdf"
)

PDF_TEMPLATE_PATH_BERITA_ACARA = os.path.join(
    os.path.dirname(__file__),
    "..", "static", "uploads",
    "kjp_format_berita_acara_page.pdf"
)

PDF_TEMPLATE_PATH_PERMOHONAN = os.path.join(
    os.path.dirname(__file__),
    "..", "static", "uploads",
    "kjp_format_permohonan_page.pdf"
)

PDF_TEMPLATE_PATH_SURAT_PERNYATAAN = os.path.join(
    os.path.dirname(__file__),
    "..", "static", "uploads",
    "kjp_format_surat_pernyataan_page.pdf"
)

views = Blueprint("dashbord_admin", __name__)

@views.route("/dashbord-admin")
@login_required
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
@login_required
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

                    # ? data murid
                    # "tanggal":    str(siswa.tanggal) or "",
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

                    # ? data wali
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
                    "rt_wali": siswa.rt_wali or "",
                    "rw_wali": siswa.rw_wali or "",
                    "provinsi_wali": siswa.provinsi_wali or "",
                    "kota_wali": siswa.kota_wali or "",
                    "kecamatan_wali": siswa.kecamatan_wali or "",
                    "kelurahan_wali": siswa.kelurahan_wali or "",
                    "kode_pos_wali": siswa.kode_pos_wali or "",
                    "status_tempat_tinggal_wali": siswa.status_tempat_tinggal_wali or "",
                    "no_hp_wali": siswa.no_hp_wali or "",
                    "no_telepon_wali": siswa.no_telepon_wali or "",
                    "tipe_alamat_wali": siswa.tipe_alamat_wali or "",

                    # ? data kontak darurat
                    "nama_kontak_darurat": siswa.nama_kontak_darurat or "",
                    "no_identitas_kontak": siswa.no_identitas_kontak or "",
                    "hubungan_kontak": siswa.hubungan_kontak or "",
                    "alamat_kontak": siswa.alamat_kontak or "",
                    "rt_kontak": siswa.rt_kontak or "",
                    "rw_kontak": siswa.rw_kontak or "",
                    "provinsi_kontak": siswa.provinsi_kontak or "",
                    "kota_kontak": siswa.kota_kontak or "",
                    "kecamatan_kontak": siswa.kecamatan_kontak or "",
                    "kelurahan_kontak": siswa.kelurahan_kontak or "",
                    "kode_pos_kontak": siswa.kode_pos_kontak or "",
                    "no_telepon_kontak": siswa.no_telepon_kontak or "",

                    # ? data permohonan
                    "nama_pemohon": siswa.nama_pemohon or "",
                    "alamat_pemohon": siswa.alamat_pemohon or "",
                    "rt_pemohon": siswa.rt_pemohon or "",
                    "rw_pemohon": siswa.rw_pemohon or "",
                    "kelurahan_pemohon": siswa.kelurahan_pemohon or "",
                    "kecamatan_pemohon": siswa.kecamatan_pemohon or "",
                    "kota_pemohon": siswa.kota_pemohon or "",
                    "kode_pos_pemohon": siswa.kode_pos_pemohon or "",
                    "telepon_pemohon": siswa.telepon_pemohon or "",
                    "nama_sekolah": siswa.nama_sekolah or "",
                    "alamat_sekolah": siswa.alamat_sekolah or "",
                    "rt_sekolah": siswa.rt_sekolah or "",
                    "rw_sekolah": siswa.rw_sekolah or "",
                    "kelurahan_sekolah": siswa.kelurahan_sekolah or "",
                    "kecamatan_sekolah": siswa.kecamatan_sekolah or "",
                    "kota_sekolah": siswa.kota_sekolah or "",
                    "kode_pos_sekolah": siswa.kode_pos_sekolah or "",
                    "ttd_pemohon": siswa.ttd_pemohon or "",

                    #? data surat pernyataan
                    "sp_nama_peserta": siswa.sp_nama_peserta or "",
                    "sp_sekolah": siswa.sp_sekolah or "",
                    "sp_kelas": siswa.sp_kelas or "",
                    "sp_nama_ortu": siswa.sp_nama_ortu or "",
                    "sp_alamat_rumah": siswa.sp_alamat_rumah or "",
                    "ttd_ortu": siswa.ttd_ortu or "",
                    "ttd_penerima": siswa.ttd_penerima or "",
                    "sptm_nama": siswa.sptm_nama or "",
                    "sptm_noktp": siswa.sptm_noktp or "",
                    "sptm_pekerjaan": siswa.sptm_pekerjaan or "",
                    "sptm_alamat": siswa.sptm_alamat or "",
                    "ttd_sptm": siswa.ttd_sptm or "",

                    #? Berita acara
                    "ba_nama_penilai": siswa.ba_nama_penilai or "",
                    "ba_jabatan_penilai": siswa.ba_jabatan_penilai or "",
                    "ba_nama_siswa": siswa.ba_nama_siswa or "",
                    "ba_nik_siswa": siswa.ba_nik_siswa or "",
                    "ba_kelas": siswa.ba_kelas or "",
                    "penilaian_1": siswa.penilaian_1 or "",
                    "penilaian_2": siswa.penilaian_2 or "",
                    "penilaian_3": siswa.penilaian_3 or "",
                    "penilaian_4": siswa.penilaian_4 or "",
                    "ttd_ba_siswa": siswa.ttd_ba_siswa or "",
                    "ttd_ba_penilai": siswa.ttd_ba_penilai or "",
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
            download_name=f"KJP_PLUS_DATA_SISWA_{datetime.now().year}.zip"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))


@views.route("/download-data-kjp-berita-acara", methods=["POST"])
@login_required
def download_data_kjp_berita_acara():
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

                    #? Berita acara
                    "ba_nama_penilai": siswa.ba_nama_penilai or "",
                    "ba_jabatan_penilai": siswa.ba_jabatan_penilai or "",
                    "ba_nama_siswa": siswa.ba_nama_siswa or "",
                    "ba_nik_siswa": siswa.ba_nik_siswa or "",
                    "ba_kelas": siswa.ba_kelas or "",
                    "penilaian_1": siswa.penilaian_1 or "",
                    "penilaian_2": siswa.penilaian_2 or "",
                    "penilaian_3": siswa.penilaian_3 or "",
                    "penilaian_4": siswa.penilaian_4 or "",
                    "ttd_ba_siswa": siswa.ttd_ba_siswa or "",
                    "ttd_ba_penilai": siswa.ttd_ba_penilai or "",
                }

                # Isi formulir PDF dengan data siswa
                pdf_bytes = fill_kjp_pdf_berita_acara(
                    siswa_dict, template_path=PDF_TEMPLATE_PATH_BERITA_ACARA)

                # Simpan PDF ke dalam ZIP dengan nama file berdasarkan nama siswa
                nama_file = (
                    siswa.nama_murid or f"siswa_{siswa.id}").replace(" ", "_")
                zf.writestr(
                    f"KJP_BERITA_ACARA_{nama_file}_{datetime.now().year}.pdf", pdf_bytes)

        zip_buffer.seek(0)

        # Kirim file ZIP ke browser untuk didownload
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"KJP_PLUS_DATA_SISWA_BERITA_ACARA_{datetime.now().year}.zip"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))


@views.route("/download-data-kjp-surat-pernyataan", methods=["POST"])
@login_required
def download_data_kjp_surat_pernyataan():
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

                    #? data surat pernyataan
                    "sp_nama_peserta": siswa.sp_nama_peserta or "",
                    "sp_sekolah": siswa.sp_sekolah or "",
                    "sp_kelas": siswa.sp_kelas or "",
                    "sp_nama_ortu": siswa.sp_nama_ortu or "",
                    "sp_alamat_rumah": siswa.sp_alamat_rumah or "",
                    "ttd_ortu": siswa.ttd_ortu or "",
                    "ttd_penerima": siswa.ttd_penerima or "",
                }

                # Isi formulir PDF dengan data siswa
                pdf_bytes = fill_kjp_pdf_surat_pernyataan(
                    siswa_dict, template_path=PDF_TEMPLATE_PATH_SURAT_PERNYATAAN)

                # Simpan PDF ke dalam ZIP dengan nama file berdasarkan nama siswa
                nama_file = (
                    siswa.nama_murid or f"siswa_{siswa.id}").replace(" ", "_")
                zf.writestr(
                    f"KJP_SURAT_PERNYATAAN_{nama_file}_{datetime.now().year}.pdf", pdf_bytes)

        zip_buffer.seek(0)

        # Kirim file ZIP ke browser untuk didownload
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"KJP_PLUS_DATA_SISWA_SURAT_PERNYATAAN_{datetime.now().year}.zip"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))


@views.route("/download-data-kjp-permohonan", methods=["POST"])
@login_required
def download_data_kjp_permohonan():
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

                    # ? data permohonan
                    "nama_pemohon": siswa.nama_pemohon or "",
                    "alamat_pemohon": siswa.alamat_pemohon or "",
                    "rt_pemohon": siswa.rt_pemohon or "",
                    "rw_pemohon": siswa.rw_pemohon or "",
                    "kelurahan_pemohon": siswa.kelurahan_pemohon or "",
                    "kecamatan_pemohon": siswa.kecamatan_pemohon or "",
                    "kota_pemohon": siswa.kota_pemohon or "",
                    "kode_pos_pemohon": siswa.kode_pos_pemohon or "",
                    "telepon_pemohon": siswa.telepon_pemohon or "",
                    "nama_sekolah": siswa.nama_sekolah or "",
                    "alamat_sekolah": siswa.alamat_sekolah or "",
                    "rt_sekolah": siswa.rt_sekolah or "",
                    "rw_sekolah": siswa.rw_sekolah or "",
                    "kelurahan_sekolah": siswa.kelurahan_sekolah or "",
                    "kecamatan_sekolah": siswa.kecamatan_sekolah or "",
                    "kota_sekolah": siswa.kota_sekolah or "",
                    "kode_pos_sekolah": siswa.kode_pos_sekolah or "",
                    "ttd_pemohon": siswa.ttd_pemohon or "",
                    "jenis_kelamin_murid": siswa.jenis_kelamin_murid or "",
                    "nama_murid": siswa.nama_murid or "",
                    "tempat_lahir_murid": siswa.tempat_lahir_murid or "",
                    "tanggal_lahir_murid": siswa.tanggal_lahir_murid or "",
                    "alamat_murid": siswa.alamat_murid or "",
                    "rt_murid": siswa.rt_murid or "",
                    "rw_murid": siswa.rw_murid or "",
                    "kota_murid": siswa.kota_murid or "",
                    "kelurahan_murid": siswa.kelurahan_murid or "",
                    "kode_pos_murid": siswa.kode_pos_murid or "",
                }

                # Isi formulir PDF dengan data siswa
                pdf_bytes = fill_kjp_pdf_permohonan(
                    siswa_dict, template_path=PDF_TEMPLATE_PATH_PERMOHONAN)

                # Simpan PDF ke dalam ZIP dengan nama file berdasarkan nama siswa
                nama_file = (
                    siswa.nama_murid or f"siswa_{siswa.id}").replace(" ", "_")
                zf.writestr(
                    f"KJP_PERMOHONAN_{nama_file}_{datetime.now().year}.pdf", pdf_bytes)

        zip_buffer.seek(0)

        # Kirim file ZIP ke browser untuk didownload
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"KJP_PLUS_DATA_SISWA_PERMOHONAN_{datetime.now().year}.zip"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))


@views.route("/download-data-ppdb", methods=["POST"])
@login_required
def download_data_ppdb():
    if request.method == "POST":
        data_ppdb = DatabaseLayananPpdb.query.all()
        list_data = []
        for data in data_ppdb:
            list_data.append({
                "tanggal": data.tanggal,
                "nama_calon_siswa": data.nama_calon_siswa,
                "no_telepon": data.no_telepon,
                "keterangan": data.keterangan
            })

        df = pd.DataFrame(list_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Data_PPDB")
        
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"DATA_PPDB_{datetime.now().year}.xlsx"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))

@views.route("/download-data-mutasi", methods=["POST"])
@login_required
def download_data_mutasi():
    if request.method == "POST":
        data_mutasi = DatabaseLayananMutasi.query.all()
        list_data = []
        for data in data_mutasi:
            list_data.append({
                "tanggal": data.tanggal,
                "nama": data.nama,
                "sekolah_asal": data.sekolah_asal,
                "no_telepon": data.no_telepon,
                "jenis_mutasi": data.jenis_mutasi,
                "keterangan": data.keterangan,
            })

        df = pd.DataFrame(list_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="DATA_MUTASI")
        
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"DATA_MUTASI_{datetime.now().year}.xlsx"
        )

    return redirect(url_for("dashbord_admin.dashbord_admin"))