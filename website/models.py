from . import db
from flask_login import UserMixin

class SecretPassword(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    secret_pw_1 = db.Column(db.String(150))
    secret_pw_2 = db.Column(db.String(150))

class DatabaseSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    nisn = db.Column(db.String(30))
    nis = db.Column(db.String(30))
    tanggal_lahir = db.Column(db.String(150))
    alamat = db.Column(db.String(255))
    no_hp = db.Column(db.String(20))
    kelas = db.Column(db.String(10))
