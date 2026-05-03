from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from flask_mail import Message
from sqlalchemy import true
from wtforms.validators import email
from .. import mail, db
from datetime import datetime
import random
import string
import dns.resolver
import re
from ..models import DatabaseKontakEmail

auth = Blueprint("kontak", __name__)

batas_kirm_per_hari = 5

def is_email_valid(email):
    # Cek format email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False, "Format email tidak valid"
    
    # Cek MX record domain
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True, "Email valid"
    except dns.resolver.NXDOMAIN:
        return False, "Domain email tidak ditemukan"
    except dns.resolver.NoAnswer:
        return False, "Domain tidak punya mail server"
    except Exception:
        return False, "Gagal memverifikasi domain email"


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def cek_batas_kirim(email):
    hari_ini = datetime.now().strftime("%Y-%m-%d")

    log = DatabaseKontakEmail.query.filter_by(
        email = email,
        tanggal=hari_ini
    ).first()

    if log is None:
        return True, 0

    if int(log.jumlah_pengiriman) >= batas_kirm_per_hari:
        return False, log.jumlah_pengiriman
    
    return True, log.jumlah_pengiriman

def update_jumlah_kirim(email):
    hari_ini = datetime.now().strftime("%Y-%m-%d")

    log = DatabaseKontakEmail.query.filter_by(
        email=email,
        tanggal=hari_ini
    ).first()

    if log is None:
        data_baru = DatabaseKontakEmail(
            email=email,
            tanggal=hari_ini,
            jumlah_pengiriman=1
        )
        db.session.add(data_baru)
    else:
        log.jumlah_pengiriman = int(log.jumlah_pengiriman) + 1
    db.session.commit()


@auth.route("/kontak", methods=["GET", "POST"])
def kirim_pesan():
    if request.method == "POST":

        # # Cek hari (0=Senin, 6=Minggu)
        hari_ini = datetime.now().weekday()
        # if hari_ini >= 5:  # 5=Sabtu, 6=Minggu
        #     flash("Pesan hanya dapat dikirim pada hari Senin - Jumat.", category="error")
        #     return redirect(url_for("kontak.kirim_pesan"))


        nama = request.form.get('nama')
        email_pengirim = request.form.get('email')
        subjek = request.form.get('subjek')
        pesan_user = request.form.get('pesan')

        # Validasi email
        valid, pesan_validasi = is_email_valid(email_pengirim)
        if not valid:
            flash(f"Email tidak valid: {pesan_validasi}", category="error")
            return redirect(url_for("kontak.kirim_pesan"))

        bisa_kirim, jumlah =cek_batas_kirim(email_pengirim)
        if not bisa_kirim:
            flash(f"Email Sudah mengirim sebanyak {batas_kirm_per_hari} kali.", category="error")
            return redirect(url_for("kontak.kirim_pesan"))

        # Simpan data form ke session
        session['nama'] = nama
        session['email_pengirim'] = email_pengirim
        session['subjek'] = subjek
        session['pesan_user'] = pesan_user

        # Kirim OTP ke email user
        otp = generate_otp()
        session['otp'] = otp

        try:
            otp_msg = Message(subject="Kode Verifikasi - Kontak Web",
                             sender=current_app.config['MAIL_USERNAME'],
                             recipients=[email_pengirim])
            otp_msg.body = f"Halo {nama},\n\nKode OTP kamu adalah: {otp}\n\nKode ini hanya berlaku untuk satu kali penggunaan."
            mail.send(otp_msg)

            flash("Kode OTP telah dikirim ke email kamu.", category="success")
            return redirect(url_for("kontak.verifikasi_otp"))

        except Exception as e:
            flash("Gagal mengirim OTP. Pastikan email kamu benar.", category="error")
            return redirect(url_for("kontak.kirim_pesan"))

    return render_template("kontak.html")


@auth.route("/verifikasi-otp", methods=["GET", "POST"])
def verifikasi_otp():
    # Jika session kosong, redirect ke halaman kontak
    if 'otp' not in session:
        flash("Sesi telah berakhir. Silakan isi form kembali.", category="error")
        return redirect(url_for("kontak.kirim_pesan"))

    if request.method == "POST":
        kode_input = request.form.get('otp')

        if kode_input == session.get('otp'):
            try:
                # OTP benar, kirim pesan asli ke admin
                msg = Message(subject=f"Kontak Web: {session['subjek']}",
                             sender=current_app.config['MAIL_USERNAME'],
                             recipients=["ahmad.andika.training1.0@gmail.com"])  # ganti dengan email kamu
                msg.body = f"Dari: {session['nama']} ({session['email_pengirim']})\n\nPesan:\n{session['pesan_user']}"
                mail.send(msg)

                update_jumlah_kirim(session["email_pengirim"])

                # Hapus semua session setelah berhasil
                session.pop('otp', None)
                session.pop('nama', None)
                session.pop('email_pengirim', None)
                session.pop('subjek', None)
                session.pop('pesan_user', None)

                flash("Pesan berhasil dikirim! Terima kasih telah menghubungi kami.\nSilahkan tunggu pesan kembali dari pihak Kami.", category="success")
                return redirect(url_for("kontak.kirim_pesan"))

            except Exception as e:
                flash("Gagal mengirim pesan. Silakan coba lagi.", category="error")
                return redirect(url_for("kontak.verifikasi_otp"))
        else:
            flash("Kode OTP salah! Silakan coba lagi.", category="error")

    return render_template("verifikasi_otp.html")
