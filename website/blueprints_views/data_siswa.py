from flask import Blueprint, render_template, redirect, url_for, request
from ..models import DatabaseSiswa
from .. import db
from flask_login import current_user

views = Blueprint("data_siswa", __name__)

@views.route("/data-siswa")
def data_siswa():
    q = request.args.get("q")

    if q:
        database_siswa = DatabaseSiswa.query.filter(
            db.or_(
                DatabaseSiswa.nama.ilike(f'%{q}%'),
                DatabaseSiswa.nisn.ilike(f'%{q}%'),
                DatabaseSiswa.nis.ilike(f'%{q}%'),
            )
        ).all()
    else:
        database_siswa = DatabaseSiswa.query.order_by(DatabaseSiswa.nis.asc()).all()
    return render_template(
                            "data-siswa.html", 
                            user=current_user, 
                            students=database_siswa, 
    )
