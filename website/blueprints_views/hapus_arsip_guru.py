from flask import Blueprint, render_template, current_app, jsonify, request, flash
from flask_login import login_required
from .. import db
from ..models import DatabaseArsipGuru
import os
import json

views = Blueprint("hapus_arsip_guru", __name__)

@views.route("/hapus-arsip-guru", methods=["POST"])
@login_required
def hapus_arsip_guru():
    guru = json.loads(request.data)
    guruId = guru["guruId"]
    guru = DatabaseArsipGuru.query.get(guruId)

    if guru:
        if guru.list_nama_data:
            for data in guru.list_nama_data:
                data_full_path = os.path.join(current_app.root_path, "static", "uploads", data)
                if os.path.exists(data_full_path):
                    os.remove(data_full_path)
        db.session.delete(guru)
        db.session.commit()
        flash("Success hapus data arsip guru.", category="success")
    return jsonify({})