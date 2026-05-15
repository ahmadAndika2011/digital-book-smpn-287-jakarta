from flask import Blueprint, render_template
from..models import DatabaseLayananKjp
from flask_login import login_required

views = Blueprint("table_kjp", __name__)

def get_data_kjp():
    database_q = DatabaseLayananKjp.query
    database_q = database_q.all()
    for kjp in database_q:
        yield kjp


@views.route("/table-kjp", methods=["GET", "POST"])
@login_required
def table_kjp():
    data = get_data_kjp()
    jumlah_siswa = DatabaseLayananKjp.query.count()
    return render_template("table-kjp.html", data=data, jumlah_siswa=jumlah_siswa)