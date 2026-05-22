from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required

from website.blueprints import feedbacks
from ..models import DatabaseFeedbacks
from .. import db

views = Blueprint("data_feedbacks", __name__)

def get_data_feedback():
    feedbacks = DatabaseFeedbacks.query.all()
    for feedback in feedbacks:
        yield feedback


@views.route("/dashbord-feedbacks")
@login_required
def dashbord_feedbacks():
    feedbacks = get_data_feedback()
    return render_template("dashbord-feedbacks.html", feedbacks=feedbacks)