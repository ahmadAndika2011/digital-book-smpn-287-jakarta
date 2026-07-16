from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipGuru, DatabaseGuru
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db


views = Blueprint("detail_arsip_guru", __name__)

@views.route("/detail-arsip-guru/<int:id>")
@login_required
def detail_arsip_guru(id):
    data = DatabaseArsipGuru.query.get(id)
    if not data:
        return "Data Arsip Guru tidak di temukan", 404
    return render_template("detail-arsip-guru.html", guru=data)

