from fileinput import filename
from unicodedata import category
from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import SecretPassword, DatabaseSiswa, NilaiSiswa
from datetime import datetime
from . import db
import os 
from werkzeug.utils import secure_filename

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password")

        user = SecretPassword.query.filter(
            (SecretPassword.secret_pw_1 == pw) |
            (SecretPassword.secret_pw_2 == pw)
        ).first()

        if user:
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            return redirect(url_for('views.home'))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/input", methods=["GET", "POST"])
@login_required
def input():
    if request.method == "POST":
        # input data Murid
        gambar_file = request.files.get("gambar")
        if gambar_file:
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            gambar_input = filename 
        else:
            gambar_input = None

        name_input = request.form.get("name")
        nisn_input = request.form.get("nisn")
        nis_input = request.form.get("nis")
        tanggal_lahir_input = request.form.get("tanggal_lahir")
        tempat_lahir_input = request.form.get("tempat_lahir")
        agama_input = request.form.get("agama")
        sekolah_asal_input = request.form.get("sekolah_asal")
        check_duplicate_nisn = DatabaseSiswa.query.filter_by(nisn=nisn_input).first()
        check_duplicate_nis = DatabaseSiswa.query.filter_by(nis=nis_input).first()
        # input Nilai Murid
        n_agama_input = request.form.get("n_agama")
        n_pancasila_input = request.form.get("n_pancasila")
        n_indonesia_input = request.form.get("n_indonesia")
        n_matematika_input = request.form.get("n_matematika")
        n_ipa_input = request.form.get("n_ipa")
        n_ips_input = request.form.get("n_ips")
        n_inggris_input = request.form.get("n_inggris")
        n_seni_budaya_input = request.form.get("n_seni_budaya")
        n_olahraga_input = request.form.get("n_olahraga")
        n_prakarya_input = request.form.get("n_prakarya")

        try:
            valid_date = datetime.strptime(tanggal_lahir_input, "%Y-%m-%d")
        except Exception as e:
            valid_date = None

        if check_duplicate_nisn:
            flash("NISN sudah ada.", category="error")
            pass
        elif check_duplicate_nis:
            flash("NIS sudah ada.", category="error")
            pass
        elif len(nisn_input) != 10:
            flash("NISN harus 10 digit.", category="error")
            pass
        elif len(nis_input) != 4:
            flash("NIS harus 4 digit.", category="error")
            pass
        elif not valid_date:
            flash("Tanggal lahir tidak valid.", category="error")
            pass
        else:
            data_siswa = DatabaseSiswa(
                image=gambar_input,
                nama=name_input,
                nisn=nisn_input,
                nis=nis_input,
                tanggal_lahir=tanggal_lahir_input,
                tempat_lahir=tempat_lahir_input,
                agama=agama_input,
                sekolah_asal=sekolah_asal_input,
            )
            nilai_siswa = NilaiSiswa(
                nisn=nisn_input,
                agama=n_agama_input,
                pancasila=n_pancasila_input,
                indonesia=n_indonesia_input,
                matematika=n_matematika_input,
                ipa=n_ipa_input,
                ips=n_ips_input,
                inggris=n_inggris_input,
                seni_budaya=n_seni_budaya_input,
                olahraga=n_olahraga_input,
                prakarya=n_prakarya_input
            )
            db.session.add(data_siswa)
            db.session.add(nilai_siswa)
            db.session.commit()
            flash("Berhasil tambah data.", category="success")

    return render_template("input.html")

@auth.route("/update-data/<int:id>", methods=["GET", "POST"])
@login_required
def update_data(id):
    student = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=student.nisn).first()

    if request.method == "POST":
        """
            data student
        """
        gambar_file = request.files.get("gambar")
        if gambar_file:
            # hapus gambar
            if student and student.image:
                image_path = os.path.join(current_app.root_path, "static/uploads", student.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # update gambar
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            student.image = filename
            flash("success update gambar.", category="success")
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")

        success_update = []

        if len(name_new) < 1:
            pass
        else:
            success_update.append("nama")
            student.nama = name_new
        if len(nisn_new) != 10:
            pass
        else:
            success_update.append("nisn")
            student.nisn = nisn_new
        if len(nis_new) != 4:
            pass
        else:
            success_update.append("nis")
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        if not valid_tanggal_lahir:
            pass
        else:
            success_update.append("tanggal lahir")
            student.tanggal_lahir = tanggal_lahir_new

        if len(tempat_lahir_new) < 1:
            pass
        else:
            success_update.append("tempat lahir")
            student.tempat_lahir = tempat_lahir_new.title()
        if not agama_new:
            pass
        else:
            success_update.append("agama")
            student.agama = agama_new
        if len(sekolah_asal_new) < 1:
            pass
        else:
            success_update.append("sekolah asal")
            student.sekolah_asal = sekolah_asal_new
        
        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(f"success update {success_update[i]}.", category="success")

        """
            Nilai student
        """
        n_agama_new = request.form.get("n_agama")
        n_pancasila_new = request.form.get("n_pancasila")
        n_indonesia_new = request.form.get("n_indonesia")
        n_matematika_new = request.form.get("n_matematika")
        n_ipa_new = request.form.get("n_ipa")
        n_ips_new = request.form.get("n_ips")
        n_inggris_new = request.form.get("n_inggris")
        n_seni_budaya_new = request.form.get("n_seni_budaya")
        n_olahraga_new = request.form.get("n_olahraga")
        n_prakarya_new = request.form.get("n_prakarya")

        success_update_n = []

        if len(n_agama_new) < 1:
            pass
        else:
            success_update_n.append("nilai agama")
            nilai_siswa.agama = n_agama_new

        if len(n_pancasila_new) < 1:
            pass
        else:
            success_update_n.append("nilai ppkn")
            nilai_siswa.pancasila = n_pancasila_new

        if len(n_indonesia_new) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa indonesia")
            nilai_siswa.indonesia = n_indonesia_new

        if len(n_matematika_new) < 1:
            pass
        else:
            success_update_n.append("nilai matematika")
            nilai_siswa.matematika = n_matematika_new

        if len(n_ipa_new) < 1:
            pass
        else:
            success_update_n.append("nilai ipa")
            nilai_siswa.ipa = n_ipa_new

        if len(n_ips_new) < 1:
            pass
        else:
            success_update_n.append("nilai ips")
            nilai_siswa.ips = n_ips_new

        if len(n_inggris_new) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa ingrris")
            nilai_siswa.inggris = n_inggris_new

        if len(n_seni_budaya_new) < 1:
            pass
        else:
            success_update_n.append("nilai seni budaya")
            nilai_siswa.seni_budaya = n_seni_budaya_new

        if len(n_olahraga_new) < 1:
            pass
        else:
            success_update_n.append("nilai olahraga")
            nilai_siswa.olahraga = n_olahraga_new

        if len(n_prakarya_new) < 1:
            pass
        else:
            success_update_n.append("nilai prakarya")
            nilai_siswa.prakarya = n_prakarya_new

        if len(success_update_n) >= 1:
            for i in range(len(success_update_n)):
                flash(f"success update {success_update_n[i]}.", category="success")
        
        db.session.commit()
        return redirect(url_for("views.home"))

    return render_template("update_data.html", user=current_user)


@auth.route("/update-data-per-student/<int:id>", methods=["GET", "POST"])
@login_required
def update_data_student(id):
    student = DatabaseSiswa.query.get(id)
    nilai_siswa = NilaiSiswa.query.filter_by(nisn=student.nisn).first()

    if request.method == "POST":
        """
            data student
        """
        gambar_file = request.files.get("gambar")
        if gambar_file:
            # hapus gambar
            if student and student.image:
                image_path = os.path.join(current_app.root_path, "static/uploads", student.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # update gambar
            filename = secure_filename(gambar_file.filename)
            upload_path = os.path.join("website", "static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            gambar_file.save(os.path.join("website/static/uploads", filename))
            student.image = filename
            flash("success update gambar.", category="success")
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")

        success_update = []

        if len(name_new) < 1:
            pass
        else:
            success_update.append("nama")
            student.nama = name_new
        if len(nisn_new) != 10:
            pass
        else:
            success_update.append("nisn")
            student.nisn = nisn_new
        if len(nis_new) != 4:
            pass
        else:
            success_update.append("nis")
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        if not valid_tanggal_lahir:
            pass
        else:
            success_update.append("tanggal lahir")
            student.tanggal_lahir = tanggal_lahir_new

        if len(tempat_lahir_new) < 1:
            pass
        else:
            success_update.append("tempat lahir")
            student.tempat_lahir = tempat_lahir_new.title()
        if not agama_new:
            pass
        else:
            success_update.append("agama")
            student.agama = agama_new
        if len(sekolah_asal_new) < 1:
            pass
        else:
            success_update.append("sekolah asal")
            student.sekolah_asal = sekolah_asal_new
        
        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(f"success update {success_update[i]}.", category="success")
        
        """
            nilai student
        """
        n_agama_new = request.form.get("n_agama")
        n_pancasila_new = request.form.get("n_pancasila")
        n_indonesia_new = request.form.get("n_indonesia")
        n_matematika_new = request.form.get("n_matematika")
        n_ipa_new = request.form.get("n_ipa")
        n_ips_new = request.form.get("n_ips")
        n_inggris_new = request.form.get("n_inggris")
        n_seni_budaya_new = request.form.get("n_seni_budaya")
        n_olahraga_new = request.form.get("n_olahraga")
        n_prakarya_new = request.form.get("n_prakarya")

        success_update_n = []

        if len(n_agama_new) < 1:
            pass
        else:
            success_update_n.append("nilai agama")
            nilai_siswa.agama = n_agama_new

        if len(n_pancasila_new) < 1:
            pass
        else:
            success_update_n.append("nilai ppkn")
            nilai_siswa.pancasila = n_pancasila_new

        if len(n_indonesia_new) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa indonesia")
            nilai_siswa.indonesia = n_indonesia_new

        if len(n_matematika_new) < 1:
            pass
        else:
            success_update_n.append("nilai matematika")
            nilai_siswa.matematika = n_matematika_new

        if len(n_ipa_new) < 1:
            pass
        else:
            success_update_n.append("nilai ipa")
            nilai_siswa.ipa = n_ipa_new

        if len(n_ips_new) < 1:
            pass
        else:
            success_update_n.append("nilai ips")
            nilai_siswa.ips = n_ips_new

        if len(n_inggris_new) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa ingrris")
            nilai_siswa.inggris = n_inggris_new

        if len(n_seni_budaya_new) < 1:
            pass
        else:
            success_update_n.append("nilai seni budaya")
            nilai_siswa.seni_budaya = n_seni_budaya_new

        if len(n_olahraga_new) < 1:
            pass
        else:
            success_update_n.append("nilai olahraga")
            nilai_siswa.olahraga = n_olahraga_new

        if len(n_prakarya_new) < 1:
            pass
        else:
            success_update_n.append("nilai prakarya")
            nilai_siswa.prakarya = n_prakarya_new

        if len(success_update_n) >= 1:
            for i in range(len(success_update_n)):
                flash(f"success update {success_update_n[i]}.", category="success")
        
        db.session.commit()
        return redirect(url_for("views.info", id=id))

    return render_template("update_data.html", user=current_user)