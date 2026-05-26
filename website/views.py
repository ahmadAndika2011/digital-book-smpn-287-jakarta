from email.utils import unquote
import os
from re import I
from traceback import print_tb
from flask import Blueprint, current_app, flash, render_template, redirect, request, url_for, jsonify, Response, abort
from functools import wraps

from website.blueprints import feedbacks
from . import db
from flask_login import login_required, current_user
from .models import DatabaseSiswa, DatabaseNilaiSiswa, AccountSiswa, AdminAccount, Berita, DatabaseGuru, DatabaseKontakEmail, DatabaseFeedbacks
import json
import base64
from datetime import datetime
from werkzeug.security import generate_password_hash

views = Blueprint("views", __name__)

# def role_required(*roles):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if current_user.role not in roles:
#                 abort(403)  # Forbidden
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator


@views.route("/sitemap.xml", methods=["GET"])
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://smpn-287-jakarta.sch.id/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
    return Response(xml, mimetype="application/xml")

@views.route("/")
def home():
    #? Create Account for admin
    # data_admin = AdminAccount(
    #     username="20107181SMPN287.",
    #     secret_pw=generate_password_hash("20107181SMPN287Jakarta!", method="pbkdf2:sha256"),
    # )
    # db.session.add(data_admin)
    # db.session.commit()

    feedbacks = DatabaseFeedbacks.query.all()

    jumlah_siswa = DatabaseSiswa.query.count()
    jumlah_guru = DatabaseGuru.query.count()

    berita_list = Berita.query.all()

    data_email = DatabaseKontakEmail.query.filter(DatabaseKontakEmail.tanggal != datetime.now().strftime("%Y-%m-%d")).all()
    if data_email:
        for email in data_email:
            db.session.delete(email)
        db.session.commit()

    return render_template("home.html", user=current_user, jumlah_siswa=jumlah_siswa, berita_list=berita_list, jumlah_guru=jumlah_guru, feedbacks=feedbacks)


#? Profil sekolah
@views.route("/profil-sekolah")
def profil_sekolah():
    jumlah_siswa = DatabaseSiswa.query.count()
    jumlah_guru = DatabaseGuru.query.count()
    return render_template("profil-sekolah.html", jumlah_siswa=jumlah_siswa, jumlah_guru=jumlah_guru)

#? Struktur organisasi
@views.route("/struktur-organisasi")
def struktur_organisasi():
    nama_kepsek = DatabaseGuru.query.filter_by(jabatan="Kepala Sekolah").first()
    akademik = DatabaseGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Akademik").first()
    kesiswaan = DatabaseGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Kesiswaan").first()
    sarpras = DatabaseGuru.query.filter_by(jabatan="Wakil Kepala Sekolah Bidang Sarpras").first()
    humas = DatabaseGuru.query.filter_by(jabatan="Humas").first()
    return render_template("struktur-organisasi.html", nama_kepsek=nama_kepsek, akademik=akademik, kesiswaan=kesiswaan, sarpras=sarpras, humas=humas)

#? Kepala Sekolah
@views.route("/kepala-sekolah")
def kepala_sekolah():
    kepsek = DatabaseGuru.query.filter_by(jabatan="Kepala Sekolah").first()
    return render_template("kepala-sekolah.html", kepsek=kepsek)

#? kurikulum
@views.route("/kurikulum")
def kurikulum():
    return render_template("kurikulum.html")

#? ekstrakurikuler
@views.route("/ekstrakurikuler")
def ekstrakurikuler():
    return render_template("ekstrakurikuler.html")

