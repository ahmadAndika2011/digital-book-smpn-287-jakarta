from flask import Blueprint, render_template, current_app, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from .. import db
from ..models import DatabaseArsipGuru
import os
import json

views = Blueprint("hapus_data_arsip_guru", __name__)

@views.route("/hapus-data-arsip-guru", methods=["POST"])
@login_required
def hapus_data_arsip_guru():
    data = request.get_json()
    guru = DatabaseArsipGuru.query.get(data["guruId"])
    if not guru:
        flash("Data tidak ada", category="error")
        return redirect(url_for("detail_arsip_guru.detail_arsip_guru", id=data["guruId"]))

    filename = data["filename"]
    filepath = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        filename
    )
    if os.path.exists(filepath):
        os.remove(filepath)

    if filename in guru.list_nama_data:
        guru.list_nama_data.remove(filename)

    db.session.commit() 
    flash("Success hapus data arsip guru.", category="success")
    return jsonify({})