from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..models import DatabaseSiswa, AccountSiswa
from werkzeug.security import generate_password_hash
from .. import db

auth = Blueprint("buat_akun_siswa", __name__)

@auth.route("/buat-akun", methods=["GET", "POST"])
def buat_akun():
    if request.method == "POST":
        nis = request.form.get("nis")
        password = request.form.get("password")
        check_nis = DatabaseSiswa.query.filter_by(nis=nis).first()
        check_nis_from_account = AccountSiswa.query.filter_by(nis=nis).first()
        if check_nis:
            if not check_nis_from_account:
                if password:
                    hash_password = generate_password_hash(password, method="pbkdf2:sha256")
                    account_siswa = AccountSiswa(
                        nis=nis,
                        password=hash_password
                    )
                    db.session.add(account_siswa)
                    db.session.commit()
                    flash("Akun berhasil dibuat!", category="success")
                    return redirect(url_for('buat_akun_siswa.buat_akun'))
                else:
                    flash("Password tidak boleh kosong!", category="error")
                    return redirect(url_for('buat_akun_siswa.buat_akun'))
            else:
                flash("Akun untuk NIS ini sudah ada!", category="error")
                return redirect(url_for('buat_akun_siswa.buat_akun'))
        else:
            flash("NIS tidak ditemukan di database!", category="error")
            return redirect(url_for('buat_akun_siswa.buat_akun'))
        
    return render_template("buat-akun.html")