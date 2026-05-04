from flask import Blueprint, render_template, flash, redirect, url_for
views = Blueprint("pilihan_layanan", __name__)

@views.route("/pilihan-layanan")
def pilihan_layanan():
    return render_template("pilihan-layanan.html")