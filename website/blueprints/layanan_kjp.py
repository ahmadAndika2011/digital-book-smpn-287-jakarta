from flask import Blueprint, render_template, redirect, flash, request, url_for
from datetime import datetime
from ..models import DatabaseLayananKjp, DatabaseSiswa
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
        # pendidikan_murid = request.form.get("pendidikan_murid")
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

        # cek tanggal lahir murid
        try:
            valid_tanggal_lahir_murid = datetime.strptime(tanggal_lahir_murid, "%Y-%m-%d")
        except:
            valid_tanggal_lahir_murid = None

        cek_nisn_murid_from_database_siswa = DatabaseSiswa.query.filter_by(nisn=nisn_murid).first()
        cek_nisn_murid_from_database_layanan_kjp = DatabaseLayananKjp.query.filter_by(nisn_murid=nisn_murid).first()

        # cek
        if cek_nisn_murid_from_database_layanan_kjp:
            flash("data anda sudah ada di dalam database, mohon tunggu...\nUntuk lebih jelas bisa kontak operator di menu kontak.", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        elif (
            len(nik_murid) != 16
            or not nama_murid
            or not jenis_kelamin_murid
            or not agama_murid
            or not tempat_lahir_murid
            or not valid_tanggal_lahir_murid
            or not nama_ibu_kandung_murid
            or not kelas
            # or not pendidikan_murid
            or (len(no_hp_murid) < 10 or len(no_hp_murid) > 12)
            or len(no_kartu_keluarga) != 16
            or not tipe_alamat
            or not status_tempat_tinggal
            or not alamat_surat
            or not rt_murid
            or not rw_murid
            or not provinsi_murid
            or not kota_murid
            or not kecamatan_murid
            or not kelurahan_murid
            or not kode_pos_murid
            or not alamat_murid
        ):
            flash("Data tidak valid.\nSilahkan cek kembali data anda", category="error")
            return redirect(url_for("layanan_kjp.layanan_kjp"))
        else:
            if not masa_berlaku_identitas:
                if  cek_nisn_murid_from_database_siswa:
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
                    )
                    db.session.add(data_kjp)
                else:
                    flash("NISN murid belum terdaftar di database siswa, silahkan gunakan menu kontak, untuk menghubungi operator.", category="error")
                    return redirect(url_for("layanan_kjp.layanan_kjp"))
            else:
                if  cek_nisn_murid_from_database_siswa:
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
                    )
                    db.session.add(data_kjp)
                else:
                    flash("NISN murid belum terdaftar di database siswa, silahkan gunakan menu kontak, untuk menghubungi operator.", category="error")
                    return redirect(url_for("layanan_kjp.layanan_kjp"))
            db.session.commit()
            flash("Success Menambahkan data.", category="success")
        return redirect(url_for("views.home"))
    return render_template("layanan-kjp.html")
