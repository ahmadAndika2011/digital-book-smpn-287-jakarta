from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipGuru, DatabaseGuru
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db

views = Blueprint("pilih_arsip_ijazah", __name__)

@views.route("/pilih-arsip-ijazah")
@login_required
def pilih_arsip_ijazah():
    daftar_tahun_ajaran = [
        {'label': '2025/2026', 'slug': '2025-2026'},
        {'label': '2026/2027', 'slug': '2026-2027'},
    ]
    return render_template("pilih-arsip-ijazah.html", daftar_tahun_ajaran=daftar_tahun_ajaran)