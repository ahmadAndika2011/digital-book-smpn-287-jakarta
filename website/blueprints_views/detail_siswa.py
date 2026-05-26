from flask import Blueprint, render_template
from ..models import DatabaseSiswa, DatabaseNilaiSiswa
from flask_login import current_user

views = Blueprint("detail_siswa", __name__)

@views.route("/info_siswa/<int:id>")
def info(id):
    database_siswa = DatabaseSiswa.query.get(id)
    nilai_siswa = DatabaseNilaiSiswa.query.filter_by(nisn=database_siswa.nisn).first()

    return render_template("info.html", user=current_user, student=database_siswa, nilai=nilai_siswa)