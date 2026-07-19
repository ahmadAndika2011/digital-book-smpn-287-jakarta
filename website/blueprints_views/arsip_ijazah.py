from website import blueprints_views
from ..models import DatabaseArsipIjazah
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, render_template
from .. import db

views = Blueprint("arsip_ijazah", __name__)

@views.route("/arsip-ijazah/<tahun_ajaran>")
@login_required
def arsip_ijazah(tahun_ajaran):
    
    arsip_ijazah = DatabaseArsipIjazah.query.filter_by(tahun=tahun_ajaran).all()
    return render_template("arsip-ijazah.html", arsip_ijazah=arsip_ijazah, tahun=tahun_ajaran)