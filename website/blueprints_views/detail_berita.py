from flask import Blueprint, render_template
from ..models import Berita

views = Blueprint("detail_berita", __name__)

@views.route("/lihat-berita/<int:id>")
def detail_berita(id):
    berita = Berita.query.get(id)
    if not berita:
        return "Berita tidak ditemukan", 404
    return render_template("lihat-berita.html", berita=berita)