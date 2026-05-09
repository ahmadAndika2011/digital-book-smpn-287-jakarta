from flask import Blueprint, render_template, current_app, jsonify, request, flash
from flask_login import login_required
from .. import db
from ..models import DatabaseGuru
import os
import json
from ..views import role_required

views = Blueprint("hapus_guru", __name__)

@views.route("/hapus-data-guru", methods=["POST"])
@login_required
@role_required("superadmin")
def hapus_guru():
    guru = json.loads(request.data)
    guruId = guru["guruId"]
    guru = DatabaseGuru.query.get(guruId)

    if guru:
        if guru.image:
            image_full_path = os.path.join(current_app.root_path, "static", "uploads", guru.image)
            if os.path.exists(image_full_path):
                os.remove(image_full_path)
        db.session.delete(guru)
        db.session.commit()
        flash("Success delete data guru.", category="success")
    return jsonify({})