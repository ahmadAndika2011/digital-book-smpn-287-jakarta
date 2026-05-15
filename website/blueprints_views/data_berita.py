from flask import Blueprint, render_template,request
from ..models import Berita
from .. import db

views = Blueprint("data_berita", __name__)

def get_berita(q=None):
    database_q = Berita.query

    if q:
        database_q = database_q.filter(
            db.or_(
                Berita.title.ilike(f"%{q}%")
            )
        ).all()
    else:
        database_q = database_q.all()
    
    for berita in database_q:
        yield berita

@views.route("/berita")
def data_berita():
    q = request.args.get("q")
    # if q:
    #     list_berita = Berita.query.filter(
    #         db.or_(
    #             Berita.title.ilike(f"%{q}%")
    #         )
    #     )
    # else:
    #     list_berita = Berita.query.all()
    list_berita = get_berita(q)
    return render_template("berita.html", list_berita=list_berita)