from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from numpy import delete
from ..models import DatabaseLayananPip
import json
from .. import db
import os

views = Blueprint("hapus_data_pip", __name__)

@views.route("/hapus-data-pip", methods=["POST"])
@login_required
def hapus_data_pip():
    data = json.loads(request.data)
    data_id = data["dataPipId"]
    data = DatabaseLayananPip.query.get(data_id)

    if data:
        if data.image_1:
            if os.path.exists(os.path.join("website/static/uploads", data.image_1)):
                os.remove(os.path.join("website/static/uploads", data.image_1))

        if data.image_2:
            if os.path.exists(os.path.join("website/static/uploads", data.image_2)):
                os.remove(os.path.join("website/static/uploads", data.image_2))
                
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data layanan PIP.", category="success")
    
    return jsonify({})