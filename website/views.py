from email.utils import unquote
import os
from re import I
from traceback import print_tb
from flask import Blueprint, current_app, flash, render_template, redirect, request, url_for, jsonify
from . import db
from flask_login import login_required, current_user
from .models import DatabaseSiswa, NilaiSiswa, AccountSiswa, AdminAccount, ImgName, DataGuru
import json
import base64

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # akun_admin = AdminAccount(
    #     username="Abdul Rohim",
    #     secret_pw="46du1_R0h1m@d1g1t4l-b00k-smpn-287-jkt-001"
    # )
    # db.session.add(akun_admin)
    # db.session.commit()
    jumlah_siswa = DatabaseSiswa.query.count()
    jumlah_guru = DataGuru.query.count()

    berita_list = ImgName.query.all()
    guru_list = DataGuru.query.all()
    return render_template("home.html", user=current_user, jumlah_siswa=jumlah_siswa, berita_list=berita_list, guru_list=guru_list, jumlah_guru=jumlah_guru)

#? Search Siswa
@views.route("/data-siswa")
def data_siswa():
    nilai_siswa = NilaiSiswa.query.all()
    
    # search program
    query = request.args.get("q", "").strip()
    if query:
        search = f"%{query}%"
        database_siswa = DatabaseSiswa.query.filter(
            db.or_(
                DatabaseSiswa.nama.ilike(search),
                DatabaseSiswa.nisn.ilike(search),
                DatabaseSiswa.nis.ilike(search),
            )
        ).all()
    else:
        database_siswa = DatabaseSiswa.query.order_by(DatabaseSiswa.nis.asc()).all()

    name = request.args.get("name")
    lulus = request.args.get("lulus")
    return render_template("data-siswa.html", user=current_user, students=database_siswa, nilai=nilai_siswa, query=query, name=name, lulus=lulus)

#? Detail Siswa
@views.route("/info_siswa/<int:id>")
def info(id):
    database_siswa = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=database_siswa.nisn).first()

    return render_template("info.html", user=current_user, student=database_siswa, nilai=nilai_siswa)

#? Detail Berita
@views.route("/lihat-berita/<int:id>")
def lihat_berita(id):
    berita = ImgName.query.get(id)
    if not berita:
        return "Berita tidak ditemukan", 404
    return render_template("lihat-berita.html", berita=berita)

#? Detail Guru
@views.route("/lihat-guru/<int:id>")
def lihat_guru(id):
    guru = DataGuru.query.get(id)
    if not guru:
        return "Data Guru tidak ditemukan", 404
    return render_template("lihat-guru.html", guru=guru)

#? Hapus Berita
@views.route("/hapus-berita", methods=["POST"])
@login_required
def hapus_berita():
    berita = json.loads(request.data)
    beritaId = berita["beritaId"]
    berita = ImgName.query.get(beritaId)
    
    if berita:
        for file_path in [berita.img_1, berita.img_2, berita.img_3, berita.video]:
            if file_path:
                full_path = os.path.join(current_app.root_path, "static", "uploads", file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
        db.session.delete(berita)
        db.session.commit()
        flash("Success hapus berita.", category="success")
    return jsonify({})

#? Hapus Data Guru
@views.route("/hapus-data-guru", methods=["POST"])
@login_required
def hapus_data_guru():
    guru = json.loads(request.data)
    guruId = guru["guruId"]
    guru = DataGuru.query.get(guruId)

    if guru:
        if guru.image:
            image_full_path = os.path.join(current_app.root_path, "static", "uploads", guru.image)
            if os.path.exists(image_full_path):
                os.remove(image_full_path)
        db.session.delete(guru)
        db.session.commit()
        flash("Success delete data guru.", category="success")
    return jsonify({})

#? Hapus Data (pribadi siswa, nilai siswa, dan akun siswa)
@views.route("/delete-student", methods=["POST"])
def delete_student():
    student = json.loads(request.data)
    studentId = student["studentId"]
    student = DatabaseSiswa.query.get(studentId)
    
    # hapus gambar
    student = DatabaseSiswa.query.get(studentId)
    if student and student.image:
        image_path = os.path.join(current_app.root_path, "static/uploads", student.image)
        if os.path.exists(image_path):
            os.remove(image_path)
        
    # Hapus account
    nis = DatabaseSiswa.query.filter_by(id=studentId).first().nis
    account_siswa = AccountSiswa.query.filter_by(nis=nis).first()

    # hapus nilai
    nisn = DatabaseSiswa.query.filter_by(id=studentId).first().nisn
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=nisn).first()

    # hapus data student
    if student and nilai_siswa:
        db.session.delete(student)
        db.session.delete(nilai_siswa)
        if account_siswa:
            db.session.delete(account_siswa)
        db.session.commit()

    return jsonify({})

#? All data guru
@views.route("/data-guru")
def data_guru():
    list_data_guru = DataGuru.query.all()
    jumlah_status_pns = DataGuru.query.filter_by(status="PNS").count()
    jumlah_status_p3k = DataGuru.query.filter_by(status="PPPK").count()
    jumlah_status_kki = DataGuru.query.filter_by(status="KKI").count()
    return render_template("data-guru.html", 
                           list_data_guru=list_data_guru, 
                           jumlah_status_pns=jumlah_status_pns, 
                           jumlah_status_kki=jumlah_status_kki, 
                           jumlah_status_p3k=jumlah_status_p3k)

#? All berita
@views.route("/berita")
def berita():
    list_berita = ImgName.query.all()
    return render_template("berita.html", list_berita=list_berita)

#? Profil sekolah
@views.route("/profil-sekolah")
def profil_sekolah():
    jumlah_siswa = DatabaseSiswa.query.count()
    jumlah_guru = DataGuru.query.count()
    return render_template("profil-sekolah.html", jumlah_siswa=jumlah_siswa, jumlah_guru=jumlah_guru)

#? Struktur organisasi
@views.route("/struktur-organisasi")
def struktur_organisasi():
    nama_kepsek = DataGuru.query.filter_by(jabatan="Kepala Sekolah").first()
    akademik = DataGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Akademik").first()
    kesiswaan = DataGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Kesiswaan").first()
    sarpras = DataGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Sarpras").first()
    humas = DataGuru.query.filter_by(jabatan="Humas").first()
    return render_template("struktur-organisasi.html", nama_kepsek=nama_kepsek, akademik=akademik, kesiswaan=kesiswaan, sarpras=sarpras, humas=humas)

#? Kepala Sekolah
@views.route("/kepala-sekolah")
def kepala_sekolah():
    kepsek = DataGuru.query.filter_by(jabatan="Kepala Sekolah").first()
    return render_template("kepala-sekolah.html", kepsek=kepsek)

#? kurikulum
@views.route("/kurikulum")
def kurikulum():
    return render_template("kurikulum.html")

#? ekstrakurikuler
@views.route("/ekstrakurikuler")
def ekstrakurikuler():
    return render_template("ekstrakurikuler.html")

#? template lulus
@views.route("/check-kelulusan")
def template_lulus():
    name = request.args.get("name")
    lulus = request.args.get("lulus")
    return render_template("template-lulus.html", name=name, lulus=lulus)

# #? Kontak
# @views.route("/kontak")
# def kontak():
#     return render_template("kontak.html")