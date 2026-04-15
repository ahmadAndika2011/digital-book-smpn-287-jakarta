from fileinput import filename

from flask import Blueprint, render_template, redirect, request_started, url_for, request, current_app
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
        kelas_input = request.form.get("kelas")
        check_duplicate_nisn = DatabaseSiswa.query.filter_by(nisn=nisn_input).first()
        check_duplicate_nis = DatabaseSiswa.query.filter_by(nis=nis_input).first()
        # input Nilai Murid
        n_agama_input = request.form.get("n_agama")
        pancasila_input = request.form.get("pancasila")
        indonesia_input = request.form.get("indonesia")
        matematika_input = request.form.get("matematika")
        ipa_input = request.form.get("ipa")
        ips_input = request.form.get("ips")
        inggris_input = request.form.get("inggris")
        seni_budaya_input = request.form.get("seni_budaya")
        olahraga_input = request.form.get("olahraga")
        prakarya_input = request.form.get("prakarya")

        try:
            valid_date = datetime.strptime(tanggal_lahir_input, "%Y-%m-%d")
        except Exception as e:
            valid_date = None

        if check_duplicate_nisn:
            pass
        elif check_duplicate_nis:
            pass
        elif len(name_input) < 1:
            pass
        elif len(nisn_input) != 10:
            pass
        elif len(nis_input) != 4:
            pass
        elif not valid_date:
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
                kelas=kelas_input
            )
            nilai_siswa = NilaiSiswa(
                nisn=nisn_input,
                agama=n_agama_input,
                pancasila=pancasila_input,
                indonesia=indonesia_input,
                matematika=matematika_input,
                ipa=ipa_input,
                ips=ips_input,
                inggris=inggris_input,
                seni_budaya=seni_budaya_input,
                olahraga=olahraga_input,
                prakarya=prakarya_input
            )
            db.session.add(data_siswa)
            db.session.add(nilai_siswa)
            db.session.commit()

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
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")
        kelas_new = request.form.get("kelas")

        # Check name
        if len(name_new) < 1:
            pass
        else:
            student.nama = name_new

        # Check nisn
        if len(nisn_new) != 10:
            pass
        else:
            student.nisn = nisn_new

        # Check nis
        if len(nis_new) != 4:
            pass
        else:
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        # Check tanggal lahir
        if not valid_tanggal_lahir:
            pass
        else:
            student.tanggal_lahir = tanggal_lahir_new

        # Check tempat lahir
        if len(tempat_lahir_new) < 1:
            pass
        else:
            student.tempat_lahir = tempat_lahir_new

        # Check alamat
        if not agama_new:
            pass
        else:
            student.agama = agama_new

        # Check no hp
        if len(sekolah_asal_new) < 1:
            pass
        else:
            student.sekolah_asal = sekolah_asal_new

        # Check kelas
        if len(kelas_new) < 1:
            pass
        else:
            student.kelas = kelas_new

        """
            Nilai student
        """
        n_agama_new = request.form.get("n_agama")
        pancasila_new = request.form.get("pancasila")
        matematika_new = request.form.get("matematika")
        ipa_new = request.form.get("ipa")
        ips_new = request.form.get("ips")
        inggris_new = request.form.get("inggris")
        seni_budaya_new = request.form.get("seni_budaya")
        olahraga_new = request.form.get("olahraga")
        prakarya_new = request.form.get("prakarya")

        if len(n_agama_new) < 1:
            pass
        else:
            nilai_siswa.agama = n_agama_new

        if len(pancasila_new) < 1:
            pass
        else:
            nilai_siswa.pancasila = pancasila_new

        if len(matematika_new) < 1:
            pass
        else:
            nilai_siswa.matematika = matematika_new

        if len(ipa_new) < 1:
            pass
        else:
            nilai_siswa.ipa = ipa_new

        if len(ips_new) < 1:
            pass
        else:
            nilai_siswa.ips = ips_new

        if len(inggris_new) < 1:
            pass
        else:
            nilai_siswa.inggris = inggris_new

        if len(seni_budaya_new) < 1:
            pass
        else:
            nilai_siswa.seni_budaya = seni_budaya_new

        if len(olahraga_new) < 1:
            pass
        else:
            nilai_siswa.olahraga = olahraga_new

        if len(prakarya_new) < 1:
            pass
        else:
            nilai_siswa.prakarya = prakarya_new
        
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
        else:
            pass

        name_new = request.form.get("name")
        nisn_new = request.form.get("nisn")
        nis_new = request.form.get("nis")
        tanggal_lahir_new = request.form.get("tanggal_lahir")
        tempat_lahir_new = request.form.get("tempat_lahir")
        agama_new = request.form.get("agama")
        sekolah_asal_new = request.form.get("sekolah_asal")
        kelas_new = request.form.get("kelas")

        # Check name
        if len(name_new) < 1:
            pass
        else:
            student.nama = name_new

        # Check nisn
        if len(nisn_new) != 10:
            pass
        else:
            student.nisn = nisn_new

        # Check nis
        if len(nis_new) != 4:
            pass
        else:
            student.nis = nis_new

        try:
            valid_tanggal_lahir = datetime.strptime(tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        # Check tanggal lahir
        if not valid_tanggal_lahir:
            pass
        else:
            student.tanggal_lahir = tanggal_lahir_new

        # Check tempat lahir
        if len(tempat_lahir_new) < 1:
            pass
        else:
            student.tempat_lahir = tempat_lahir_new

        # Check agama
        if not agama_new:
            pass
        else:
            student.agama = agama_new

        # Check no hp
        if len(sekolah_asal_new) < 1:
            pass
        else:
            student.sekolah_asal = sekolah_asal_new

        # Check kelas
        if len(kelas_new) < 1:
            pass
        else:
            student.kelas = kelas_new
        
        """
            nilai student
        """
        n_agama_new = request.form.get("n_agama")
        pancasila_new = request.form.get("pancasila")
        matematika_new = request.form.get("matematika")
        ipa_new = request.form.get("ipa")
        ips_new = request.form.get("ips")
        inggris_new = request.form.get("inggris")
        seni_budaya_new = request.form.get("seni_budaya")
        olahraga_new = request.form.get("olahraga")
        prakarya_new = request.form.get("prakarya")

        if len(n_agama_new) < 1:
            pass
        else:
            nilai_siswa.agama = n_agama_new

        if len(pancasila_new) < 1:
            pass
        else:
            nilai_siswa.pancasila = pancasila_new

        if len(matematika_new) < 1:
            pass
        else:
            nilai_siswa.matematika = matematika_new

        if len(ipa_new) < 1:
            pass
        else:
            nilai_siswa.ipa = ipa_new

        if len(ips_new) < 1:
            pass
        else:
            nilai_siswa.ips = ips_new

        if len(inggris_new) < 1:
            pass
        else:
            nilai_siswa.inggris = inggris_new

        if len(seni_budaya_new) < 1:
            pass
        else:
            nilai_siswa.seni_budaya = seni_budaya_new

        if len(olahraga_new) < 1:
            pass
        else:
            nilai_siswa.olahraga = olahraga_new

        if len(prakarya_new) < 1:
            pass
        else:
            nilai_siswa.prakarya = prakarya_new
        
        db.session.commit()
        return redirect(url_for("views.info", id=id))

    return render_template("update_data.html", user=current_user)