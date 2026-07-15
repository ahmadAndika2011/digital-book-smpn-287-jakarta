from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from ..models import DatabaseSiswa, DatabaseNilaiSiswa, DatabaseLegerSiswa
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
from .. import db

auth = Blueprint("update_data_siswa", __name__)

ALLOWED_FORMAT = ["xlsx", "xls", "csv"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMAT

@auth.route("/update-data/<int:id>", methods=["GET", "POST"])
@login_required
def update_data(id):
    student = DatabaseSiswa.query.get(id)
    nilai_siswa = DatabaseNilaiSiswa.query.filter_by(nisn_siswa=student.nisn).first()
    leger_siswa = DatabaseLegerSiswa.query.filter_by(nisn=student.nisn).first()
    agama_siswa = ["Islam", "Kristen", "Katolik", "Hindu", 'Buddha', 'Konghucu']
    lulus=["Ya", "Tidak"]

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

        if len(success_update) >= 1:
            for i in range(len(success_update)):
                flash(
                    f"success update {success_update[i]}.", category="success")

        """
            Nilai student
        """
        file = request.files.get("upload_nilai")

        if file and file.filename != "":
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

        """
            LEGER SISWA
        """
        leger_agama_kristen = request.form.get("leger_agama_kristen")
        leger_agama_islam = request.form.get("leger_agama_islam")
        leger_pkn = request.form.get("leger_pkn")
        leger_b_indo = request.form.get("leger_b_indo")
        leger_matematika = request.form.get("leger_matematika")
        leger_ipa = request.form.get("leger_ipa")
        leger_ips = request.form.get("leger_ips")
        leger_b_inggris = request.form.get("leger_b_inggris")
        leger_seni_budaya = request.form.get("leger_seni_budaya")
        leger_pjok = request.form.get("leger_pjok")
        leger_informatika = request.form.get("leger_informatika")
        leger_sakit = request.form.get("leger_sakit")
        leger_izin = request.form.get("leger_izin")
        leger_alpha = request.form.get("leger_alpha")
        leger_rohkris = request.form.get("leger_rohkris")
        leger_rohis = request.form.get("leger_rohis")
        leger_basket = request.form.get("leger_basket")
        leger_takraw = request.form.get("leger_takraw")
        leger_futsal = request.form.get("leger_futsal")
        leger_silat = request.form.get("leger_silat")
        leger_taekwondo = request.form.get("leger_taekwondo")
        leger_pramuka = request.form.get("leger_pramuka")
        leger_pmr = request.form.get("leger_pmr")
        leger_marching_band = request.form.get("leger_marching_band")
        
        success_update_n = []
        
        if len(leger_marching_band) < 1:
            pass
        else:
            success_update_n.append("marching band")
            leger_siswa.marching_band = leger_marching_band
        
        if len(leger_pmr) < 1:
            pass
        else:
            success_update_n.append("pmr")
            leger_siswa.pmr = leger_pmr
        
        if len(leger_pramuka) < 1:
            pass
        else:
            success_update_n.append("pramuka")
            leger_siswa.pramuka = leger_pramuka
        
        if len(leger_taekwondo) < 1:
            pass
        else:
            success_update_n.append("taekwondo")
            leger_siswa.taekwondo = leger_taekwondo
        
        if len(leger_silat) < 1:
            pass
        else:
            success_update_n.append("silat")
            leger_siswa.silat = leger_silat
        
        if len(leger_futsal) < 1:
            pass
        else:
            success_update_n.append("fotsal")
            leger_siswa.futsal = leger_futsal
        
        if len(leger_takraw) < 1:
            pass
        else:
            success_update_n.append("takraw")
            leger_siswa.takraw = leger_takraw
        
        if len(leger_basket) < 1:
            pass
        else:
            success_update_n.append("basket")
            leger_siswa.basket = leger_basket
        
        if len(leger_rohis) < 1:
            pass
        else:
            success_update_n.append("rohis")
            leger_siswa.rohis = leger_rohis
        
        if len(leger_rohkris) < 1:
            pass
        else:
            success_update_n.append("rohkris")
            leger_siswa.rohkris = leger_rohkris

        if len(leger_alpha) < 1:
            pass
        else:
            success_update_n.append("alpha")
            leger_siswa.alpha = leger_alpha
        
        if len(leger_izin) < 1:
            pass
        else:
            success_update_n.append("izin")
            leger_siswa.izin = leger_izin
        
        if len(leger_sakit) < 1:
            pass
        else:
            success_update_n.append("alpha")
            leger_siswa.sakit = leger_sakit

        if len(leger_informatika) < 1:
            pass
        else:
            success_update_n.append("nilai informatika")
            leger_siswa.informatika = leger_informatika
        
        if len(leger_pjok) < 1:
            pass
        else:
            success_update_n.append("nilai pjok")
            leger_siswa.pjok = leger_pjok
        
        if len(leger_seni_budaya) < 1:
            pass
        else:
            success_update_n.append("nilai seni budaya")
            leger_siswa.seni_budaya = leger_seni_budaya
        
        if len(leger_b_inggris) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa inggris")
            leger_siswa.b_inggris = leger_b_inggris
        
        if len(leger_ips) < 1:
            pass
        else:
            success_update_n.append("nilai ips")
            leger_siswa.ips = leger_ips
        
        if len(leger_ipa) < 1:
            pass
        else:
            success_update_n.append("nilai ipa")
            leger_siswa.ipa = leger_ipa
        
        if len(leger_matematika) < 1:
            pass
        else:
            success_update_n.append("nilai matematika")
            leger_siswa.matematika = leger_matematika
        
        if len(leger_b_indo) < 1:
            pass
        else:
            success_update_n.append("nilai bahasa indonesia")
            leger_siswa.b_indo = leger_b_indo
        
        if len(leger_pkn) < 1:
            pass
        else:
            success_update_n.append("nilai pkn")
            leger_siswa.pkn = leger_pkn
        
        if len(leger_agama_islam) < 1:
            pass
        else:
            success_update_n.append("nilai agama islam")
            leger_siswa.agama_islam = leger_agama_islam
        
        if len(leger_agama_kristen) < 1:
            pass
        else:
            success_update_n.append("nilai agama kristen")
            leger_siswa.agama_kristen = leger_agama_kristen
        
        if len(success_update_n) >= 1:
            for i in range(len(success_update_n)):
                flash(
                    f"success update {success_update_n[i]}.", category="success")

        db.session.commit()
        return redirect(url_for("data_siswa.data_siswa"))

    return render_template("update_data.html", user=current_user, student=student, nilai_siswa=nilai_siswa, leger_siswa=leger_siswa, agama_siswa=agama_siswa, siswa_lulus=lulus)