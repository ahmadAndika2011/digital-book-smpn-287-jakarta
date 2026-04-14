from enum import unique

from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGBLOB  

class SecretPassword(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    secret_pw_1 = db.Column(db.String(150))
    secret_pw_2 = db.Column(db.String(150))


class DatabaseSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255))
    nama = db.Column(db.String(150))
    nisn = db.Column(db.String(30))
    nis = db.Column(db.String(30))
    tanggal_lahir = db.Column(db.String(150))
    tempat_lahir = db.Column(db.String(150))
    agama = db.Column(db.String(50))
    sekolah_asal = db.Column(db.String(20))
    kelas = db.Column(db.String(10))

class NilaiSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.String(30))
    agama = db.Column(db.String(50))
    pancasila = db.Column(db.String(50))
    indonesia = db.Column(db.String(50))
    matematika = db.Column(db.String(50))
    ipa = db.Column(db.String(50))
    ips = db.Column(db.String(50))
    inggris = db.Column(db.String(50))
    seni_budaya = db.Column(db.String(50))
    olahraga = db.Column(db.String(50))
    prakarya = db.Column(db.String(50))