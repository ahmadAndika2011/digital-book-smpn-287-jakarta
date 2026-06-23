from flask import Blueprint, render_template, current_app, jsonify, request, flash
from flask_login import login_required
from .. import db
from ..models import DatabaseTendik
import os
import json

views = Blueprint("hapus_tendik", __name__)

@views.route("/hapus-data-tendik", methods=["POST"])
@login_required
def hapus_tendik():
    guru = json.loads(request.data)
    guruId = guru["guruId"]
    guru = DatabaseTendik.query.get(guruId)

    if guru:
        if guru.image:
            image_full_path = os.path.join(current_app.root_path, "static", "uploads", guru.image)
            if os.path.exists(image_full_path):
                os.remove(image_full_path)
        db.session.delete(guru)
        db.session.commit()
        flash("Success delete data tendik.", category="success")
    return jsonify({})