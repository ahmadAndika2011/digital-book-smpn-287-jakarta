from flask import Blueprint, render_template, request, jsonify, json, current_app
import os
from ..views import role_required
from .. import db
from ..models import DatabaseSiswa, AccountSiswa, NilaiSiswa

views = Blueprint("hapus_siswa", __name__)

@views.route("/delete-student", methods=["POST"])
@role_required("superadmin")
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