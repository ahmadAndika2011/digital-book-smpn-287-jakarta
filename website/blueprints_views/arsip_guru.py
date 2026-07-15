from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from ..models import DatabaseArsipGuru, DatabaseGuru
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from .. import db

views = Blueprint("arsip_guru", __name__)

@views.route("/arsip-guru")
def arsip_guru():
    arsip_guru = DatabaseArsipGuru.query.all()

    return render_template("arsip-guru.html", arsip_guru=arsip_guru)