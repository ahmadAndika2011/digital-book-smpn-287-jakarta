import base64
from email import header
import os
from PIL import Image
from flask import Blueprint, current_app, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananKjp, DatabaseSiswa
from .. import db
from io import BytesIO

auth = Blueprint("layanan_kjp", __name__)


# ???????????????????????????????????????????????????????????????????????????????????????????????????????????/
@auth.route("/layanan-kjp", methods=["GET", "POST"])
def layanan_kjp():
    if request.method == "POST":
        # ? data siswa
        nik_murid = request.form.get("nik_murid")
        nama_murid = request.form.get("nama_murid")
        jenis_kelamin_murid = request.form.get("jenis_kelamin_murid")
        agama_murid = request.form.get("agama_murid")
        tempat_lahir_murid = request.form.get("tempat_lahir_murid")
        tanggal_lahir_murid = request.form.get("tanggal_lahir_murid")
        nama_ibu_kandung_murid = request.form.get("nama_ibu_kandung_murid")
        kelas = request.form.get("kelas")
        nisn_murid = request.form.get("nisn_murid")
        no_hp_murid = request.form.get("no_hp_murid")
        no_telepon = request.form.get("no_telepon")
        masa_berlaku_identitas = request.form.get("masa_berlaku_identitas")
        untuk_disabilitas = request.form.get("untuk_disabilitas")
        no_kartu_keluarga = request.form.get("no_kartu_keluarga")
        tipe_alamat = request.form.get("tipe_alamat")
        status_tempat_tinggal = request.form.get("status_tempat_tinggal")
        alamat_surat = request.form.get("alamat_surat")
        rt_murid = request.form.get("rt_murid")
        rw_murid = request.form.get("rw_murid")
        provinsi_murid = request.form.get("provinsi_murid").upper()
        kota_murid = request.form.get("kota_murid").upper()
        kecamatan_murid = request.form.get("kecamatan_murid").upper()
        kelurahan_murid = request.form.get("kelurahan_murid").upper()
        kode_pos_murid = request.form.get("kode_pos_murid")
        npwp_murid = request.form.get("npwp_murid")
        alamat_murid = request.form.get("alamat_murid")
        #* cek tanggal lahir murid
        try:
            valid_tanggal_lahir_murid = datetime.strptime(tanggal_lahir_murid, "%Y-%m-%d")
        except:
            valid_tanggal_lahir_murid = None
        #* Cek
        cek_nisn_murid_from_database_siswa = DatabaseSiswa.query.filter_by(nisn=nisn_murid).first()
        cek_nisn_murid_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(nisn_murid=nisn_murid).first()
        cek_npwp_murid_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(npwp_murid=npwp_murid).first()
        cek_nik_murid_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(nik_murid=nik_murid).first()
        cek_no_kartu_keluarga_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(no_kartu_keluarga=no_kartu_keluarga).first()

        # ? data wali
        nama_wali = request.form.get("nama_wali")
        no_ktp_wali = request.form.get("no_ktp_wali")
        masa_berlaku_ktp_wali = request.form.get("masa_berlaku_ktp_wali")
        npwp_wali = request.form.get("npwp_wali")
        kartu_keluarga_wali = request.form.get("kartu_keluarga_wali")
        tempat_lahir_wali = request.form.get("tempat_lahir_wali")
        tanggal_lahir_wali = request.form.get("tanggal_lahir_wali")
        jenis_kelamin_wali = request.form.get("jenis_kelamin_wali")
        agama_wali = request.form.get("agama_wali")
        nama_ibu_kandung_wali = request.form.get("nama_ibu_kandung_wali")
        pekerjaan_wali = request.form.get("pekerjaan_wali")
        status_pernikahan_wali = request.form.get("status_pernikahan_wali")
        pendidikan_wali = request.form.get("pendidikan_wali")
        jabatan_wali = request.form.get("jabatan_wali")
        alamat_wali = request.form.get("alamat_wali")
        rt_wali = request.form.get("rt_wali")
        rw_wali = request.form.get("rw_wali")
        provinsi_wali = request.form.get("provinsi_wali")
        kota_wali = request.form.get("kota_wali")
        kecamatan_wali = request.form.get("kecamatan_wali")
        kelurahan_wali = request.form.get("kelurahan_wali")
        kode_pos_wali = request.form.get("kode_pos_wali")
        status_tempat_tinggal_wali = request.form.get("status_tempat_tinggal_wali")
        no_hp_wali = request.form.get("no_hp_wali")
        no_telepon_wali = request.form.get("no_telepon_wali")
        tipe_alamat_wali = request.form.get("tipe_alamat_wali")
        #* Cek
        cek_no_ktp_wali_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(no_ktp_wali=no_ktp_wali).first()
        cek_npwp_wali_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(npwp_wali=npwp_wali).first()
        cek_kartu_keluarga_wali_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(kartu_keluarga_wali=kartu_keluarga_wali).first()

        # ? kontak darurat
        nama_kontak_darurat = request.form.get("nama_kontak_darurat")
        no_identitas_kontak = request.form.get("no_identitas_kontak")
        hubungan_kontak = request.form.get("hubungan_kontak")
        alamat_kontak = request.form.get("alamat_kontak")
        rt_kontak = request.form.get("rt_kontak")
        rw_kontak = request.form.get("rw_kontak")
        provinsi_kontak = request.form.get("provinsi_kontak")
        kota_kontak = request.form.get("kota_kontak")
        kecamatan_kontak = request.form.get("kecamatan_kontak")
        kelurahan_kontak = request.form.get("kelurahan_kontak")
        kode_pos_kontak = request.form.get("kode_pos_kontak")
        no_telepon_kontak = request.form.get("no_telepon_kontak")
        #* Cek
        cek_no_identitas_kontak_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(no_identitas_kontak=no_identitas_kontak).first()

        # ? permohonan
        nama_pemohon = request.form.get("nama_pemohon", "")
        alamat_pemohon = request.form.get("alamat_pemohon", "")
        rt_pemohon = request.form.get("rt_pemohon", "")
        rw_pemohon = request.form.get("rw_pemohon", "")
        kelurahan_pemohon = request.form.get("kelurahan_pemohon", "")
        kecamatan_pemohon = request.form.get("kecamatan_pemohon", "")
        kota_pemohon = request.form.get("kota_pemohon", "")
        kode_pos_pemohon = request.form.get("kode_pos_pemohon", "")
        telepon_pemohon = request.form.get("telepon_pemohon", "")
        nama_sekolah = request.form.get("nama_sekolah", "")
        alamat_sekolah = request.form.get("alamat_sekolah", "")
        rt_sekolah = request.form.get("rt_sekolah", "")
        rw_sekolah = request.form.get("rw_sekolah", "")
        kelurahan_sekolah = request.form.get("kelurahan_sekolah", "")
        kecamatan_sekolah = request.form.get("kecamatan_sekolah", "")
        kota_sekolah = request.form.get("kota_sekolah", "")
        kode_pos_sekolah = request.form.get("kode_pos_sekolah", "")
        ttd_pemohon = request.form.get("ttd_pemohon", "")

    # ? pernyataan
        sp_nama_peserta = request.form.get("sp_nama_peserta")
        sp_sekolah = request.form.get("sp_sekolah")
        sp_kelas = request.form.get("sp_kelas")
        sp_nama_ortu = request.form.get("sp_nama_ortu")
        sp_alamat_rumah = request.form.get("sp_alamat_rumah")
        ttd_ortu = request.form.get("ttd_ortu")
        ttd_penerima = request.form.get("ttd_penerima")
        sptm_nama = request.form.get("sptm_nama")
        sptm_noktp = request.form.get("sptm_noktp")
        sptm_pekerjaan = request.form.get("sptm_pekerjaan")
        sptm_alamat = request.form.get("sptm_alamat")
        ttd_sptm = request.form.get("ttd_sptm")
        cek_no_ktp_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(sptm_noktp=sptm_noktp).first()


        # cek
        if cek_nisn_murid_from_database_layanan_kjp:
            flash("data anda sudah ada di dalam database, mohon tunggu...\nUntuk lebih jelas bisa kontak operator di menu kontak.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        if cek_no_ktp_from_database_layanan_kjp:
            flash("No KTP anda sudah terdaftar di layanan kjp.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif not cek_nisn_murid_from_database_siswa:
            flash("NISN belum terdaftar di database", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_npwp_murid_from_database_layanan_kjp:
            flash("NPWP Wali sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_nik_murid_from_database_layanan_kjp:
            flash("NIK Siswa sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_no_kartu_keluarga_from_database_layanan_kjp:
            flash("No kartu keluarga siswa sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_no_ktp_wali_from_database_layanan_kjp:
            flash("No KTP wali sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_npwp_wali_from_database_layanan_kjp:
            flash("NPWP wali sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_kartu_keluarga_wali_from_database_layanan_kjp:
            flash("Kartu Keluarga wali sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif cek_no_identitas_kontak_from_database_layanan_kjp:
            flash("No identitas kontak darurat sudah terdaftar di layanan kjp", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif not ttd_pemohon:
            flash("Mohon masukkan tanda tangan!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(nik_murid) != 16:
            flash("NIK tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(no_kartu_keluarga) != 16:
            flash("No Kartu Keluarga tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(nisn_murid) != 10:
            flash("NISN tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kode_pos_murid) != 5:
            flash("Kode pos tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            not nama_murid
            or not jenis_kelamin_murid
            or not agama_murid
            or not tempat_lahir_murid
            or not valid_tanggal_lahir_murid
            or not nama_ibu_kandung_murid
            or not kelas
            or (len(no_hp_murid) < 10 or len(no_hp_murid) > 12)
            or not tipe_alamat
            or not status_tempat_tinggal
            or not alamat_surat
            or not rt_murid
            or not rw_murid
            or not provinsi_murid
            or not kota_murid
            or not kecamatan_murid
            or not kelurahan_murid
            or not alamat_murid
        ):
            flash("Data murid tidak valid.\nSilahkan cek kembali data anda", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(no_ktp_wali) != 16:
            flash("No KTP Wali tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(npwp_wali) != 16:
            flash("NPWP Wali tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kartu_keluarga_wali) != 16:
            flash("No Kartu Keluarga Wali tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(no_hp_wali) < 10 or len(no_hp_wali) > 12:
            flash("No HP Wali tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kode_pos_wali) != 5:
            flash("Kode Pos Wali tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            not nama_wali
            or not jenis_kelamin_wali
            or not agama_wali
            or not tempat_lahir_wali
            or not tanggal_lahir_wali
            or not nama_ibu_kandung_wali
            or not pekerjaan_wali
            or not status_pernikahan_wali
            or not pendidikan_wali
            or not alamat_wali
            or not rt_wali
            or not rw_wali
            or not provinsi_wali
            or not kota_wali
            or not kecamatan_wali
            or not kelurahan_wali
            or not status_tempat_tinggal_wali
            or not tipe_alamat_wali
        ):
            flash("Data wali tidak valid.\nSilahkan cek kembali data wali anda", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            not nama_kontak_darurat
            or not hubungan_kontak
            or not alamat_kontak
            or not rt_kontak
            or not rw_kontak
            or not provinsi_kontak
            or not kota_kontak
            or not kecamatan_kontak
            or not kelurahan_kontak
        ):
            flash("Data kontak darurat tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(no_identitas_kontak) != 16:
            flash("No identitas untuk kontak darurat tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kode_pos_kontak) != 5:
            flash("Kode pos untuk kontak darurat tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(no_telepon_kontak) < 10 or len(no_telepon_kontak) > 12:
            flash("No telepon untuk kontak darurat tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            not nama_pemohon
            or not alamat_pemohon
            or not rt_pemohon
            or not rw_pemohon
            or not kelurahan_pemohon
            or not kecamatan_pemohon
            or not kota_pemohon
            or not nama_sekolah
            or not alamat_sekolah
            or not rt_sekolah
            or not rw_sekolah
            or not kelurahan_sekolah
            or not kecamatan_sekolah
            or not kota_sekolah
        ):
            flash("Data permohonantidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif  len(telepon_pemohon) < 10 or len(telepon_pemohon) > 12:
            flash("No telepon tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kode_pos_pemohon) != 5:
            flash("Kode pos untuk surat permohonan tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(kode_pos_sekolah) != 5:
            flash("Kode pos sekolah untuk surat permohonan tidak valid.\n Silahkan cek kebali data kontak darurat anda.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            not sp_nama_peserta 
            or not sp_sekolah
            or not sp_kelas
            or not sp_nama_ortu
            or not sp_alamat_rumah
            or not sptm_nama
            or not sptm_pekerjaan
            or not sptm_alamat
        ):
            flash("Data pernyataan ketaatan tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif not ttd_ortu:
            flash("Tanda tangan orang tua untuk Data pernyataan ketaatan tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif not ttd_penerima:
            flash("Tanda tangan penerima untuk Data pernyataan ketaatan tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif not ttd_sptm:
            flash("Tanda tangan pembuat pernyataan untuk Data pernyataan ketaatan tidak valid!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif len(sptm_noktp) != 16:
            flash("No KTP wali murid harus terdiri dari 16 digit!", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        else:
            header, encoded = ttd_pemohon.split(",", 1)
            image_data = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_data))
            save_path = os.path.join(
                current_app.root_path, "static", "uploads", "ttd")
            os.makedirs(save_path, exist_ok=True)
            filename = f"ttd_{npwp_wali}_ttd_permohonan.png"
            image.save(os.path.join(save_path, filename))
            ttd_pemohon = f"ttd_{npwp_wali}_ttd_permohonan.png"

            header, encoded = ttd_ortu.split(",", 1)
            image_data = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_data))
            save_path = os.path.join(
                current_app.root_path, "static", "uploads", "ttd")
            os.makedirs(save_path, exist_ok=True)
            filename = f"ttd_{npwp_wali}_ttd_ortu.png"
            image.save(os.path.join(save_path, filename))
            ttd_ortu = f"ttd_{npwp_wali}_ttd_ortu.png"

            header, encoded = ttd_penerima.split(",", 1)
            image_data = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_data))
            save_path = os.path.join(
                current_app.root_path, "static", "uploads", "ttd")
            os.makedirs(save_path, exist_ok=True)
            filename = f"ttd_{npwp_wali}_ttd_penerima.png"
            image.save(os.path.join(save_path, filename))
            ttd_penerima = f"ttd_{npwp_wali}_ttd_penerima.png"

            header, encoded = ttd_sptm.split(",", 1)
            image_data = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_data))
            save_path = os.path.join(
                current_app.root_path, "static", "uploads", "ttd")
            os.makedirs(save_path, exist_ok=True)
            filename = f"ttd_{npwp_wali}_ttd_sptm.png"
            image.save(os.path.join(save_path, filename))
            ttd_sptm = f"ttd_{npwp_wali}_ttd_sptm.png"

            if not masa_berlaku_identitas:
                data_kjp = DatabaseLayananKjp(
                    nik_murid = nik_murid,
                    no_kartu_keluarga = no_kartu_keluarga,
                    nama_murid = nama_murid.title(),
                    jenis_kelamin_murid = jenis_kelamin_murid,
                    tempat_lahir_murid = tempat_lahir_murid.title(),
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
                    pendidikan = "SMP",
                    untuk_disabilitas = untuk_disabilitas,
                    alamat_murid=alamat_murid,
                    rt_murid = rt_murid,
                    rw_murid = rw_murid,
                    provinsi_murid = provinsi_murid,
                    kota_murid = kota_murid,
                    kecamatan_murid = kecamatan_murid,
                    kelurahan_murid = kelurahan_murid,
                    kode_pos_murid = kode_pos_murid,
                    npwp_murid = npwp_murid,

                    # data wali
                    nama_wali = nama_wali,
                    no_ktp_wali = no_ktp_wali,
                    masa_berlaku_ktp_wali = masa_berlaku_ktp_wali,
                    npwp_wali = npwp_wali,
                    kartu_keluarga_wali = kartu_keluarga_wali,
                    tempat_lahir_wali = tempat_lahir_wali,
                    tanggal_lahir_wali = tanggal_lahir_wali,
                    jenis_kelamin_wali = jenis_kelamin_wali,
                    agama_wali = agama_wali,
                    nama_ibu_kandung_wali = nama_ibu_kandung_wali,
                    pekerjaan_wali = pekerjaan_wali,
                    status_pernikahan_wali = status_pernikahan_wali,
                    pendidikan_wali = pendidikan_wali,
                    jabatan_wali = jabatan_wali,
                    alamat_wali = alamat_wali,
                    rt_wali = rt_wali,
                    rw_wali = rw_wali,
                    provinsi_wali = provinsi_wali,
                    kota_wali = kota_wali,
                    kecamatan_wali = kecamatan_wali,
                    kelurahan_wali = kelurahan_wali,
                    kode_pos_wali = kode_pos_wali,
                    status_tempat_tinggal_wali = status_tempat_tinggal_wali,
                    no_hp_wali = no_hp_wali,
                    no_telepon_wali = no_telepon_wali,
                    tipe_alamat_wali = tipe_alamat_wali,

                    # Kontak darurat
                    nama_kontak_darurat = nama_kontak_darurat,
                    no_identitas_kontak = no_identitas_kontak,
                    hubungan_kontak = hubungan_kontak,
                    alamat_kontak = alamat_kontak,
                    rt_kontak = rt_kontak,
                    rw_kontak = rw_kontak,
                    provinsi_kontak = provinsi_kontak,
                    kota_kontak = kota_kontak,
                    kecamatan_kontak = kecamatan_kontak,
                    kelurahan_kontak = kelurahan_kontak,
                    kode_pos_kontak = kode_pos_kontak,
                    no_telepon_kontak = no_telepon_kontak,

                    # permohonan
                    nama_pemohon = nama_pemohon,
                    alamat_pemohon = alamat_pemohon,
                    rt_pemohon = rt_pemohon,
                    rw_pemohon = rw_pemohon,
                    kelurahan_pemohon = kelurahan_pemohon,
                    kecamatan_pemohon = kecamatan_pemohon,
                    kota_pemohon = kota_pemohon,
                    kode_pos_pemohon = kode_pos_pemohon,
                    telepon_pemohon = telepon_pemohon,
                    nama_sekolah = nama_sekolah,
                    alamat_sekolah = alamat_sekolah,
                    rt_sekolah = rt_sekolah,
                    rw_sekolah = rw_sekolah,
                    kelurahan_sekolah = kelurahan_sekolah,
                    kecamatan_sekolah = kecamatan_sekolah,
                    kota_sekolah = kota_sekolah,
                    kode_pos_sekolah = kode_pos_sekolah,
                    ttd_pemohon = ttd_pemohon,

                    # Pernyataan ketaatan
                    sp_nama_peserta = sp_nama_peserta,
                    sp_sekolah = sp_sekolah,
                    sp_kelas = sp_kelas,
                    sp_nama_ortu = sp_nama_ortu,
                    sp_alamat_rumah = sp_alamat_rumah,
                    ttd_ortu = ttd_ortu,
                    ttd_penerima = ttd_penerima,
                    sptm_nama = sptm_nama,
                    sptm_noktp = sptm_noktp,
                    sptm_pekerjaan = sptm_pekerjaan,
                    sptm_alamat = sptm_alamat,
                    ttd_sptm = ttd_sptm,
                )
                db.session.add(data_kjp)
            else:
                data_kjp = DatabaseLayananKjp(
                    nik_murid = nik_murid,
                    no_kartu_keluarga = no_kartu_keluarga,
                    nama_murid = nama_murid.title(),
                    jenis_kelamin_murid = jenis_kelamin_murid,
                    tempat_lahir_murid = tempat_lahir_murid.title(),
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
                    pendidikan = "SMP",
                    untuk_disabilitas = untuk_disabilitas,
                    alamat_murid=alamat_murid,
                    rt_murid = rt_murid,
                    rw_murid = rw_murid,
                    provinsi_murid = provinsi_murid,
                    kota_murid = kota_murid,
                    kecamatan_murid = kecamatan_murid,
                    kelurahan_murid = kelurahan_murid,
                    kode_pos_murid = kode_pos_murid,
                    npwp_murid = npwp_murid,

                    # data wali
                    nama_wali = nama_wali,
                    no_ktp_wali = no_ktp_wali,
                    masa_berlaku_ktp_wali = masa_berlaku_ktp_wali,
                    npwp_wali = npwp_wali,
                    kartu_keluarga_wali = kartu_keluarga_wali,
                    tempat_lahir_wali = tempat_lahir_wali,
                    tanggal_lahir_wali = tanggal_lahir_wali,
                    jenis_kelamin_wali = jenis_kelamin_wali,
                    agama_wali = agama_wali,
                    nama_ibu_kandung_wali = nama_ibu_kandung_wali,
                    pekerjaan_wali = pekerjaan_wali,
                    status_pernikahan_wali = status_pernikahan_wali,
                    pendidikan_wali = pendidikan_wali,
                    jabatan_wali = jabatan_wali,
                    alamat_wali = alamat_wali,
                    rt_wali = rt_wali,
                    rw_wali = rw_wali,
                    provinsi_wali = provinsi_wali,
                    kota_wali = kota_wali,
                    kecamatan_wali = kecamatan_wali,
                    kelurahan_wali = kelurahan_wali,
                    kode_pos_wali = kode_pos_wali,
                    status_tempat_tinggal_wali = status_tempat_tinggal_wali,
                    no_hp_wali = no_hp_wali,
                    no_telepon_wali = no_telepon_wali,
                    tipe_alamat_wali = tipe_alamat_wali,

                    # Kontak darurat
                    nama_kontak_darurat = nama_kontak_darurat,
                    no_identitas_kontak = no_identitas_kontak,
                    hubungan_kontak = hubungan_kontak,
                    alamat_kontak = alamat_kontak,
                    rt_kontak = rt_kontak,
                    rw_kontak = rw_kontak,
                    provinsi_kontak = provinsi_kontak,
                    kota_kontak = kota_kontak,
                    kecamatan_kontak = kecamatan_kontak,
                    kelurahan_kontak = kelurahan_kontak,
                    kode_pos_kontak = kode_pos_kontak,
                    no_telepon_kontak = no_telepon_kontak,

                    # permohonan
                    nama_pemohon = nama_pemohon,
                    alamat_pemohon = alamat_pemohon,
                    rt_pemohon = rt_pemohon,
                    rw_pemohon = rw_pemohon,
                    kelurahan_pemohon = kelurahan_pemohon,
                    kecamatan_pemohon = kecamatan_pemohon,
                    kota_pemohon = kota_pemohon,
                    kode_pos_pemohon = kode_pos_pemohon,
                    telepon_pemohon = telepon_pemohon,
                    nama_sekolah = nama_sekolah,
                    alamat_sekolah = alamat_sekolah,
                    rt_sekolah = rt_sekolah,
                    rw_sekolah = rw_sekolah,
                    kelurahan_sekolah = kelurahan_sekolah,
                    kecamatan_sekolah = kecamatan_sekolah,
                    kota_sekolah = kota_sekolah,
                    kode_pos_sekolah = kode_pos_sekolah,
                    ttd_pemohon = ttd_pemohon,

                    # Pernyataan ketaatan
                    sp_nama_peserta = sp_nama_peserta,
                    sp_sekolah = sp_sekolah,
                    sp_kelas = sp_kelas,
                    sp_nama_ortu = sp_nama_ortu,
                    sp_alamat_rumah = sp_alamat_rumah,
                    ttd_ortu = ttd_ortu,
                    ttd_penerima = ttd_penerima,
                    sptm_nama = sptm_nama,
                    sptm_noktp = sptm_noktp,
                    sptm_pekerjaan = sptm_pekerjaan,
                    sptm_alamat = sptm_alamat,
                    ttd_sptm = ttd_sptm,
                )
                db.session.add(data_kjp)
            db.session.commit()
            flash("Success Menambahkan data.", category="success")
        return redirect(url_for("views.home"))
    return render_template("layanan-kjp.html")
