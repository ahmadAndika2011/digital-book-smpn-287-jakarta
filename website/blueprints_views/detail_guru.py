from flask import Blueprint, render_template
from ..models import DatabaseGuru

views = Blueprint("detail_guru", __name__)

@views.route("/lihat-guru/<int:id>")
def detail_guru(id):
    guru = DatabaseGuru.query.get(id)
    if not guru:
        return "Data Guru tidak ditemukan", 404
    return render_template("lihat-guru.html", guru=guru)