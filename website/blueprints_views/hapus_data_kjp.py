from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from numpy import delete
from ..models import DatabaseLayananKjp
import json
from .. import db

views = Blueprint("hapus_data_kjp", __name__)

@views.route("/hapus-data-kjp", methods=["POST"])
@login_required
def hapus_data_kjp():
    data = json.loads(request.data)
    data_id = data["dataKjpId"]
    data = DatabaseLayananKjp.query.get(data_id)

    if data:
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data KJP.", category="success")

    return jsonify({})