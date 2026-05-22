from flask import Blueprint, render_template, flash, redirect, request, url_for
from ..models import DatabaseFeedbacks
from .. import db

auth = Blueprint("feedbacks", __name__)

@auth.route("/feedback-user", methods=["POST"])
def feedbacks():
    if request.method == 'POST':
        nama = request.form.get('nama')
        sebagai = request.form.get('sebagai')
        layanan = request.form.get('layanan')
        tingkat_kepuasan = request.form.get('tingkat_kepuasan')
        saran = request.form.get('saran')

        if not nama:
            flash("Masukkan nama anda.", category="error")
            return redirect(url_for("views.home"))
        elif not sebagai:
            flash("Pilih peran anda.", category="error")
            return redirect(url_for("views.home"))
        elif not layanan:
            flash("Pilih layanan yang ingin anda nilai.", category="error")
            return redirect(url_for("views.home"))
        elif not tingkat_kepuasan:
            flash("Pilih tingkat kepuasan anda.", category="error")
            return redirect(url_for("views.home"))
        else:
            feedback = DatabaseFeedbacks(
                nama=nama,
                sebagai=sebagai,
                layanan=layanan,
                tingkat_kepuasan=tingkat_kepuasan,
                saran=saran
            )
            db.session.add(feedback)
            db.session.commit()
            flash("Success menambahkan Survei kepuasan.", category="success")
            return redirect(url_for("views.home"))

        return redirect(url_for("views.home"))