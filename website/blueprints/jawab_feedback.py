from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required
from ..models import DatabaseFeedbacks
from .. import db

auth = Blueprint("jawab_feedback", __name__)

@auth.route("/jawab-feedback/<int:id>", methods=["GET", "POST"])
@login_required
def jawab_feedback(id):
    feedback = DatabaseFeedbacks.query.get(id)

    if request.method == "POST":
        jawaban_admin = request.form.get("jawaban_admin")
        feedback.jawaban = jawaban_admin
        db.session.commit()
        flash("Success menambahkan jawaban.", category="success")
        return redirect(url_for("data_feedbacks.dashbord_feedbacks"))
    return render_template("jawab-feedback.html", feedback=feedback)