from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
import pandas as pd
from ..models import DatabaseSiswa, NilaiSiswa
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .. import db

auth = Blueprint("update_data_per_siswa", __name__)

ALLOWED_FORMAT = ["xlsx", "xls", "csv"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

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
                image_path = os.path.join(
                    current_app.root_path, "static/uploads", student.image)
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
        alamat_new = request.form.get("alamat")
        rt_new = request.form.get("rt")
        rw_new = request.form.get("rw")
        kelurahan_new = request.form.get("kelurahan")
        kecamatan_new = request.form.get("kecamatan")
        sekolah_asal_new = request.form.get("sekolah_asal")
        lulus_new = request.form.get("lulus")

        success_update = []

                #? Update Nama
        if name_new:
            success_update.append("nama")
            student.nama = name_new

        #? Update NISN
        if len(nisn_new) != 10:
            pass
        else:
            success_update.append("nisn")
            student.nisn = nisn_new

        #? Update NIS
        if len(nis_new) != 4:
            pass
        else:
            success_update.append("nis")
            student.nis = nis_new

        #? Update Tanggal Lahir
        try:
            valid_tanggal_lahir = datetime.strptime(
                tanggal_lahir_new, "%Y-%m-%d")
        except:
            valid_tanggal_lahir = None
        if not valid_tanggal_lahir:
            pass
        else:
            success_update.append("tanggal lahir")
            student.tanggal_lahir = tanggal_lahir_new

        #? Update Tempat Lahir
        if tempat_lahir_new:
            success_update.append("tempat lahir")
            student.tempat_lahir = tempat_lahir_new.title()

        #? Update Agama
        if agama_new:
            success_update.append("agama")
            student.agama = agama_new

        #? Update Alamat
        if alamat_new:
            success_update.append("alamat")
            student.alamat = alamat_new

        #? Update Rt
        if rt_new:
            success_update.append("rt")
            student.rt = rt_new

        #? Update Rw
        if rw_new:
            success_update.append("rw")
            student.rw = rw_new

        #? Update Rw
        if kelurahan_new:
            success_update.append("kelurahan")
            student.kelurahan = kelurahan_new

        #? Update Rw
        if kecamatan_new:
            success_update.append("kecamatan")
            student.kecamatan = kecamatan_new

        #? Update Sekolah Asal
        if sekolah_asal_new:
            success_update.append("sekolah asal")
            student.sekolah_asal = sekolah_asal_new

        #? Update Lulus
        if lulus_new:
            success_update.append("lulus")
            student.lulus = lulus_new.title()
        # if len(name_new) < 1:
        #     pass
        # else:
        #     success_update.append("nama")
        #     student.nama = name_new
        # if len(nisn_new) != 10:
        #     pass
        # else:
        #     success_update.append("nisn")
        #     student.nisn = nisn_new
        # if len(nis_new) != 4:
        #     pass
        # else:
        #     success_update.append("nis")
        #     student.nis = nis_new

        # try:
        #     valid_tanggal_lahir = datetime.strptime(
        #         tanggal_lahir_new, "%Y-%m-%d")
        # except:
        #     valid_tanggal_lahir = None
        # if not valid_tanggal_lahir:
        #     pass
        # else:
        #     success_update.append("tanggal lahir")
        #     student.tanggal_lahir = tanggal_lahir_new

        # if len(tempat_lahir_new) < 1:
        #     pass
        # else:
        #     success_update.append("tempat lahir")
        #     student.tempat_lahir = tempat_lahir_new.title()
        # if not agama_new:
        #     pass
        # else:
        #     success_update.append("agama")
        #     student.agama = agama_new
        # if len(sekolah_asal_new) < 1:
        #     pass
        # else:
        #     success_update.append("sekolah asal")
        #     student.sekolah_asal = sekolah_asal_new
        # if len(lulus_new) < 1:
        #     pass
        # else:
        #     success_update.append("lulus")
        #     student.lulus = lulus_new.title()

        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(
                    f"success update {success_update[i]}.", category="success")

        """
            nilai student
        """
        file = request.files.get("upload_nilai")
        if file and file.filename:
            if allowed_file(file.filename):
                uploads_folder = current_app.config["UPLOADS_FOLDER"]
                save_path = os.path.join(uploads_folder, file.filename)
                file.save(save_path)
                flash("Nilai berhasil disimpan.", category="success")
                filename = secure_filename(file.filename)
                if filename.endswith(".csv"):
                    df_nilai_siswa = pd.read_csv(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                else:
                    df_nilai_siswa = pd.read_excel(save_path)
                    nilai_siswa.agama=str(df_nilai_siswa["agama"].iloc[0])
                    nilai_siswa.pancasila=str(df_nilai_siswa["pancasila"].iloc[0])
                    nilai_siswa.indonesia=str(df_nilai_siswa["indonesia"].iloc[0])
                    nilai_siswa.matematika=str(df_nilai_siswa["matematika"].iloc[0])
                    nilai_siswa.ipa=str(df_nilai_siswa["ipa"].iloc[0])
                    nilai_siswa.ips=str(df_nilai_siswa["ips"].iloc[0])
                    nilai_siswa.inggris=str(df_nilai_siswa["inggris"].iloc[0])
                    nilai_siswa.seni_budaya=str(df_nilai_siswa["seni_budaya"].iloc[0])
                    nilai_siswa.olahraga=str(df_nilai_siswa["olahraga"].iloc[0])
                    nilai_siswa.prakarya=str(df_nilai_siswa["prakarya"].iloc[0])
                os.remove(save_path)
        else:
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
                    flash(
                        f"success update {success_update_n[i]}.", category="success")

        db.session.commit()
        return redirect(url_for("views.info", id=id))

    return render_template("update_data.html", user=current_user)