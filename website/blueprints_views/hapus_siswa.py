from flask import Blueprint, render_template, request, jsonify, json, current_app
import os
from .. import db
from ..models import DatabaseSiswa, AccountSiswa, DatabaseNilaiSiswa

views = Blueprint("hapus_siswa", __name__)

@views.route("/delete-student", methods=["POST"])
def hapus_siswa():
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
    nisn = DatabaseSiswa.query.filter_by(id=studentId).first()
    nilai_siswa = DatabaseNilaiSiswa.query.filter_by(nisn_siswa=nisn).first()

    # hapus data student
    if student :
        if nilai_siswa:
            db.session.delete(nilai_siswa)
        db.session.delete(student)
        if account_siswa:
            db.session.delete(account_siswa)
        db.session.commit()

    return jsonify({})