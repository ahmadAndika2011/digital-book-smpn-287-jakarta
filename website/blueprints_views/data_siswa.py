from flask import Blueprint, render_template, redirect, url_for, request
from ..models import DatabaseSiswa
from .. import db
from flask_login import current_user

views = Blueprint("data_siswa", __name__)

def get_data_siswa(q=None):
    database_q = DatabaseSiswa.query

    if q:
        database_q = database_q.filter(
            db.or_(
                DatabaseSiswa.nama.ilike(f'%{q}%'),
                DatabaseSiswa.nisn.ilike(f'%{q}%'),
                DatabaseSiswa.nis.ilike(f'%{q}%'),
            )
        ).all()
    else:
        database_q = DatabaseSiswa.query.order_by(DatabaseSiswa.nis.asc()).all()

    for siswa in database_q:
        yield siswa

@views.route("/data-siswa")
def data_siswa():
    q = request.args.get("q", "").strip()

    database_siswa = get_data_siswa(q)
    return render_template(
                            "data-siswa.html", 
                            user=current_user, 
                            students=database_siswa, 
    )
