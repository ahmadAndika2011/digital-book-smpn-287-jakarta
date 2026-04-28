from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename
from .. import db
from ..models import ImgName

auth = Blueprint("input_berita", __name__)

@auth.route("/tambah-berita", methods=["GET", "POST"])
@login_required
def tambah_berita():
    if request.method == "POST":
        gambar_1_file = request.files.get("gambar_1")
        if gambar_1_file:
            filename = secure_filename(gambar_1_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_1_file.save(os.path.join(upload_path, filename))
            gambar_1_input = filename
        else:
            gambar_1_input = None
            
        gambar_2_file = request.files.get("gambar_2")
        if gambar_2_file:
            filename = secure_filename(gambar_2_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_2_file.save(os.path.join(upload_path, filename))
            gambar_2_input = filename
        else:
            gambar_2_input = ""

        gambar_3_file = request.files.get("gambar_3")
        if gambar_3_file:
            filename = secure_filename(gambar_3_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_3_file.save(os.path.join(upload_path, filename))
            gambar_3_input = filename
        else:
            gambar_3_input = ""

        video = request.files.get("video")
        if video:
            filename = secure_filename(video.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            video.save(os.path.join(upload_path, filename))
            video_input = filename
        else:
            video_input = ""

        text_input = request.form.get("keterangan")

        if text_input:
            input_berita = ImgName(
                name = text_input,
                img_1 = gambar_1_input,
                img_2 = gambar_2_input,
                img_3 = gambar_3_input,
                video = video_input
            )
            db.session.add(input_berita)
            db.session.commit()
            flash("Success Tambah berita.", category="success")
            return redirect(url_for("views.home"))

    return render_template("input-berita.html", user=current_user)