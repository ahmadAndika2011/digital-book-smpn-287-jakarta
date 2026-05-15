from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from ..models import DatabaseLayananMutasi
import json
from .. import db

views = Blueprint("hapus_data_mutasi", __name__)

@views.route("/hapus-data-mutasi", methods=["POST"])
@login_required
def hapus_data_mutasi():
    data = json.loads(request.data)
    data_id = data["dataMutasiId"]
    data = DatabaseLayananMutasi.query.get(data_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data layanan mutasi.", category="success")

    return jsonify({})