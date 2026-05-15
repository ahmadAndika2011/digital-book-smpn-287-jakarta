from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from numpy import delete

from ..models import DatabaseLayananKjp
import json
from .. import db
import os

views = Blueprint("hapus_data_kjp", __name__)

@views.route("/hapus-data-kjp", methods=["POST"])
@login_required
def hapus_data_kjp():
    data = json.loads(request.data)
    data_id = data["dataKjpId"]
    data = DatabaseLayananKjp.query.get(data_id)

    if data:
        if data.ttd_pemohon:
            image_path = os.path.join(current_app.root_path, "static/uploads/ttd", data.ttd_pemohon)
            if os.path.exists(image_path):
                os.remove(image_path)

        if data.ttd_ortu:
            image_path = os.path.join(current_app.root_path, "static/uploads/ttd", data.ttd_ortu)
            if os.path.exists(image_path):
                os.remove(image_path)

        if data.ttd_penerima:
            image_path = os.path.join(current_app.root_path, "static/uploads/ttd", data.ttd_penerima)
            if os.path.exists(image_path):
                os.remove(image_path)

        if data.ttd_sptm:
            image_path = os.path.join(current_app.root_path, "static/uploads/ttd", data.ttd_sptm)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data KJP.", category="success")

    return jsonify({})