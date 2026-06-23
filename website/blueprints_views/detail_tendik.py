from flask import Blueprint, render_template
from ..models import DatabaseTendik

views = Blueprint("detail_tendik", __name__)

@views.route("/lihat-tendik/<int:id>")
def detail_tendik(id):
    guru = DatabaseTendik.query.get(id)
    if not guru:
        return "Data Tendik tidak ditemukan", 404
    return render_template("lihat-tendik.html", guru=guru)