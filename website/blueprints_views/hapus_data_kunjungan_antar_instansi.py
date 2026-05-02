from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request, views
from flask_login import current_user, login_required
from ..models import DatabaseLayananKunjunganAntarInstansi
import json
from .. import db

views = Blueprint("hapus_data_kunjungan_antar_instansi", __name__)

@views.route("/hapus-data-kunjungan-antar-instansi", methods=["POST"])
@login_required
def hapus_data_kunjungan_antar_instansi():
    data = json.loads(request.data)
    data_id = data["dataKunjunganAntarInstansiId"]
    data = DatabaseLayananKunjunganAntarInstansi.query.get(data_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data Kunjungan Antar Instansi.", category="success")
    
    return jsonify({})