import os
from flask import Blueprint, current_app, render_template, redirect, request, url_for, jsonify
from . import db
from flask_login import login_required, current_user
from .models import DatabaseSiswa, NilaiSiswa, AccountSiswa, AdminAccount
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
    return render_template("home.html", jumlah_siswa=jumlah_siswa)

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


@views.route("/info_siswa/<int:id>")
def info(id):
    database_siswa = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=database_siswa.nisn).first()

    return render_template("info.html", user=current_user, student=database_siswa, nilai=nilai_siswa)

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
