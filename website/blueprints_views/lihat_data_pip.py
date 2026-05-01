from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import DatabaseLayananPip

views = Blueprint("lihat_data_pip", __name__)

@views.route("/lihat-data-pip/<int:id>")
def lihat_data_pip(id):
    data = DatabaseLayananPip.query.get(id)
    return f"Hi {data.nama}"