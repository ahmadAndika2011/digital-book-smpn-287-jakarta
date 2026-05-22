from flask import Blueprint, render_template, current_app, jsonify, request, flash
from flask_login import login_required
from .. import db
from ..models import DatabaseFeedbacks
import os
import json

views = Blueprint("hapus_feedback", __name__)

@views.route("/hapus-feedback", methods=["POST"])
@login_required
def hapus_feedback():
    feedback = json.loads(request.data)
    feedback_id = feedback["feedbackId"]
    feedback = DatabaseFeedbacks.query.get(feedback_id)

    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        flash("Success hapus feedback.", category="success")
    return jsonify({})