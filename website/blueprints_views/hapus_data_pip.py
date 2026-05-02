from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from numpy import delete
from ..models import DatabaseLayananPip
import json
from .. import db

views = Blueprint("hapus_data_pip", __name__)

@views.route("/hapus-data-pip", methods=["POST"])
@login_required
def hapus_data_pip():
    data = json.loads(request.data)
    data_id = data["dataPipId"]
    data = DatabaseLayananPip.query.get(data_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data layanan PIP.", category="success")
    
    return jsonify({})