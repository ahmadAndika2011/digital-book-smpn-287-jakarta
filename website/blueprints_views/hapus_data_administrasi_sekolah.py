from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from numpy import delete
from ..models import DatabaseLayananAdministrasiSekolah
import json
from .. import db

views = Blueprint("hapus_data_administrasi_sekolah", __name__)

@views.route("/hapus-data-administrasi-sekolah", methods=["POST"])
@login_required
def hapus_data_administrasi_sekolah():
    data = json.loads(request.data)
    data_id = data["dataAdministrasiSekolahId"]
    data = DatabaseLayananAdministrasiSekolah.query.get(data_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data layanan administrasi.", category="success")

    return jsonify({})