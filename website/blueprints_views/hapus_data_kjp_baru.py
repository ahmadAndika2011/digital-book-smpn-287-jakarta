from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from numpy import delete

from ..models import DatabaseLayananKjpBaru
import json
from .. import db
import os

views = Blueprint("hapus_data_kjp_baru", __name__)

@views.route("/hapus-data-kjp-baru", methods=["POST"])
@login_required
def hapus_data_kjp_baru():
    data = json.loads(request.data)
    data_id = data["dataKjpId"]
    data = DatabaseLayananKjpBaru.query.get(data_id)

    if data:
        if data.sekolah_kk:
            image_path = os.path.join(current_app.root_path, "static/uploads", data.sekolah_kk)
            if os.path.exists(image_path):
                os.remove(image_path)
        print(image_path)
        print(os.path.exists(image_path))
  
        if data.ttd_tanda_tangan:
            image_path = os.path.join(current_app.root_path, "static/uploads", data.ttd_tanda_tangan)
            if os.path.exists(image_path):
                os.remove(image_path)
        print(image_path)
        print(os.path.exists(image_path))
  
        if data.pernyataan_ttd_orang_tua:
            image_path = os.path.join(current_app.root_path, "static/uploads", data.pernyataan_ttd_orang_tua)
            if os.path.exists(image_path):
                os.remove(image_path)
        print(image_path)
        print(os.path.exists(image_path))
  
        if data.pernyataan_ttd_penerima:
            image_path = os.path.join(current_app.root_path, "static/uploads", data.pernyataan_ttd_penerima)
            if os.path.exists(image_path):
                os.remove(image_path)
        print(image_path)
        print(os.path.exists(image_path))
        
        db.session.delete(data)
        db.session.commit()
        flash("Success hapus data KJP.", category="success")

    return jsonify({})