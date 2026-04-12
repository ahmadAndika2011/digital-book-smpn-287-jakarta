from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from .models import SecretPassword
from . import db
from flask_login import login_required, current_user
from .models import DatabaseSiswa
import json
import base64

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # """
    #     Hanya Dijalankan sekali
    #     1. *(&^!*((&!!)!*iiaa89aj2882z@@)10@((joeoe9191wkjaahshgsfaya2hwwy72yw
    #     2. 8172829(*(jjjnkka&^81LLLppa8j111o2oisjsjsehhejaasdhsjhaso))
    # """
    # secret_pw = SecretPassword(
    #   secret_pw_1="*(&^!*((&!!)!*iiaa89aj2882z@@)10@((joeoe9191wkjaahshgsfaya2hwwy72yw", 
    #   secret_pw_2="8172829(*(jjjnkka&^81LLLppa8j111o2oisjsjsehhejaasdhsjhaso))"
    # )
    # db.session.add(secret_pw)
    # db.session.commit()

    database_siswa = DatabaseSiswa.query.all()


    return render_template("home.html", user=current_user, students=database_siswa)

@views.route("/info_siswa/<int:id>")
def info(id):
    database_siswa = DatabaseSiswa.query.get(id)

    return render_template("info.html", user=current_user, student=database_siswa)

@views.route("/delete-student", methods=["POST"])
def delete_student():
    student = json.loads(request.data)
    studentId = student["studentId"]
    student = DatabaseSiswa.query.get(studentId)
    if student:
        db.session.delete(student)
        db.session.commit()

    return jsonify({})