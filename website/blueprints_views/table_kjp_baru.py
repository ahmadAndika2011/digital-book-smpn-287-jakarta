from flask import Blueprint, render_template
from..models import DatabaseLayananKjpBaru
from flask_login import login_required

views = Blueprint("table_kjp_baru", __name__)

def get_data_kjp():
    database_q = DatabaseLayananKjpBaru.query
    database_q = database_q.all()
    for kjp in database_q:
        yield kjp


@views.route("/table-kjp-baru", methods=["GET", "POST"])
@login_required
def table_kjp_baru():
    data = get_data_kjp()
    jumlah_siswa = DatabaseLayananKjpBaru.query.count()
    return render_template("table-kjp-baru.html", data=data, jumlah_siswa=jumlah_siswa)