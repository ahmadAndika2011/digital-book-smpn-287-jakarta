from flask import Blueprint, render_template
from..models import DatabaseLayananKjp

views = Blueprint("table_kjp", __name__)

@views.route("/table-kjp", methods=["GET", "POST"])
def table_kjp():
    data = DatabaseLayananKjp.query.all()
    return render_template("table-kjp.html", data=data)