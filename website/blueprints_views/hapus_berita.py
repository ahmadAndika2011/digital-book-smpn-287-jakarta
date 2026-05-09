from flask import Blueprint, render_template, request, current_app, jsonify, flash
from flask_login import login_required
from ..views import role_required
from .. import db
import os
from ..models import Berita
import json


views = Blueprint("hapus_berita", __name__)

@views.route("/hapus-berita", methods=["POST"])
@login_required
@role_required("superadmin", "berita")
def hapus_berita():
    berita = json.loads(request.data)
    beritaId = berita["beritaId"]
    berita = Berita.query.get(beritaId)
    
    if berita:
        for file_path in [berita.img_1, berita.img_2, berita.img_3, berita.video]:
            if file_path:
                full_path = os.path.join(current_app.root_path, "static", "uploads", file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
        db.session.delete(berita)
        db.session.commit()
        flash("Success hapus berita.", category="success")
    return jsonify({})