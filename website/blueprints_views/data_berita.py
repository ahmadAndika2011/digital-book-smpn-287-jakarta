from flask import Blueprint, render_template,request
from ..models import Berita
from .. import db

views = Blueprint("data_berita", __name__)

@views.route("/berita")
def data_berita():
    q = request.args.get("q")
    if q:
        list_berita = Berita.query.filter(
            db.or_(
                Berita.title.ilike(f"%{q}%")
            )
        )
    else:
        list_berita = Berita.query.all()
    return render_template("berita.html", list_berita=list_berita)