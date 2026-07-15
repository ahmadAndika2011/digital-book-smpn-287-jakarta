from flask import Blueprint, render_template, request
from ..models import DatabaseNilaiSiswa, DatabaseSiswa

views = Blueprint("template_lulus", __name__)

# @views.route("/check-kelulusan")
# def template_lulus():
#     name = request.args.get("name")
#     lulus = request.args.get("lulus")

#     data_siswa = DatabaseSiswa.query.filter_by(nama = name).first()
#     data_nilai_siswa = DatabaseNilaiSiswa.query.filter_by(nama_siswa = name).first()

#     return render_template("template-lulus.html", name=name, lulus=lulus, data_siswa = data_siswa, data_nilai_siswa = data_nilai_siswa)