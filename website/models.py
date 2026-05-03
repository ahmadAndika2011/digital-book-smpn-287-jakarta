from email.policy import default
from enum import unique

from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGBLOB  

class AdminAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    secret_pw = db.Column(db.String(150))


class DatabaseSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255))
    nama = db.Column(db.String(150))
    nisn = db.Column(db.String(30))
    nis = db.Column(db.String(30))
    tempat_lahir = db.Column(db.String(150))
    tanggal_lahir = db.Column(db.String(150))
    agama = db.Column(db.String(50))
    alamat = db.Column(db.String(300))
    rt = db.Column(db.String(20))
    rw = db.Column(db.String(20))
    kelurahan = db.Column(db.String(200))
    kecamatan = db.Column(db.String(200))
    sekolah_asal = db.Column(db.String(150))
    lulus = db.Column(db.String(20))


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


class AccountSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(50))
    password = db.Column(db.String(200))

class Berita(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(350))
    describe = db.Column(db.String(350))
    img_1 = db.Column(db.String(255))
    img_2 = db.Column(db.String(255))
    img_3 = db.Column(db.String(255))
    video = db.Column(db.String(300))

class DatabaseGuru(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255))
    name = db.Column(db.String(150))
    mapel = db.Column(db.String(100))
    nip = db.Column(db.String(18))
    nrk = db.Column(db.String(6))
    status = db.Column(db.String(100))
    jabatan = db.Column(db.String(100))
    tahun_masuk = db.Column(db.String(100))

class DatabaseLayananPpdb(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama_calon_siswa = db.Column(db.String(200))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))

class DatabaseLayananMutasi(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama = db.Column(db.String(200))
    sekolah_asal = db.Column(db.String(200))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))
    jenis_mutasi = db.Column(db.String(150))

class DatabaseLayananPip(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama = db.Column(db.String(200))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))
    image_1 = db.Column(db.String(255))
    image_2 = db.Column(db.String(255))

class DatabaseLayananKjp(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama = db.Column(db.String(200))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))

class DatabaseLayananAdministrasiSekolah(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal_pengajuan = db.Column(db.String(150))
    nama = db.Column(db.String(200))
    tanggal_pengambilan = db.Column(db.String(150))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))

class DatabaseLayananKunjunganAntarInstansi(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama = db.Column(db.String(200))
    jabatan = db.Column(db.String(150))
    no_telepon = db.Column(db.String(20))
    keterangan = db.Column(db.String(300))

class DatabaseKontakEmail(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300))
    tanggal = db.Column(db.String(150))
    jumlah_pengiriman = db.Column(db.Integer, default=0)