from flask import Blueprint, render_template, current_app, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from .. import db
from ..models import DatabaseArsipIjazah
import os
import json

views = Blueprint("hapus_data_arsip_ijazah", __name__)

@views.route("/hapus-data-arsip-ijazah", methods=["POST"])
@login_required
def hapus_data_arsip_ijazah():
    data = request.get_json()
    data_ijazah = DatabaseArsipIjazah.query.get(data["id"])
    if not data_ijazah:
        flash("Data tidak ada", category="error")
        return redirect(url_for("detail_arsip_guru.detail_arsip_guru", id=data["id"]))

    filename = data["filename"]
    filepath = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        filename
    )
    if os.path.exists(filepath):
        os.remove(filepath)

    # os.remove(filepath)

    db.session.delete(data_ijazah) 
    db.session.commit() 
    flash("Success hapus data arsip ijazah.", category="success")
    return jsonify({})