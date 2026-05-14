from flask import Blueprint, render_template
from..models import DatabaseLayananKjp
from flask_login import login_required
from ..views import role_required

views = Blueprint("table_kjp", __name__)

@views.route("/table-kjp", methods=["GET", "POST"])
@login_required
def table_kjp():
    data = DatabaseLayananKjp.query.all()
    return render_template("table-kjp.html", data=data)