from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from ..models import DatabaseLayananPpdb
import json
from .. import db

views = Blueprint("hapus_data_ppdb", __name__)

@views.route("/hapus-data-ppdb", methods=["POST"])
@login_required
def hapus_data_ppdb():
    data = json.loads(request.data)
    dataId = data["dataPpdbId"]
    data = DatabaseLayananPpdb.query.get(dataId)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data layanan ppdb.", category="success")
    
    return jsonify({})