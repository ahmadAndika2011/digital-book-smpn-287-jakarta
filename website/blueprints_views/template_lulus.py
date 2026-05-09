from flask import Blueprint, render_template, request

views = Blueprint("template_lulus", __name__)

@views.route("/check-kelulusan")
def template_lulus():
    name = request.args.get("name")
    lulus = request.args.get("lulus")
    return render_template("template-lulus.html", name=name, lulus=lulus)