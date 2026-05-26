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


class DatabaseNilaiSiswa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(150))
    nisn_siswa = db.Column(db.String(30))
    agama = db.Column(db.String(50))
    pancasila = db.Column(db.String(50))
    indonesia = db.Column(db.String(50))
    matematika = db.Column(db.String(50))
    ipa = db.Column(db.String(50))
    ips = db.Column(db.String(50))
    inggris = db.Column(db.String(50))
    seni_tari = db.Column(db.String(50))
    olahraga = db.Column(db.String(50))
    tik = db.Column(db.String(50))
    rata_rata = db.Column(db.String(50))


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
    link_youtube=db.Column(db.String(2048))


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

class DatabaseFeedbacks(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150))
    sebagai = db.Column(db.String(150))
    layanan = db.Column(db.String(150))
    tingkat_kepuasan = db.Column(db.String(150))
    saran = db.Column(db.String(300))
    jawaban = db.Column(db.String(300))


class DatabaseLayananPpdb(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(150))
    nama_calon_siswa = db.Column(db.String(200))
    no_telepon = db.Column(db.String(20))
    keperluan = db.Column(db.String(300))
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
    # .. kolom yang sudah ada ...
    id = db.Column(db.Integer, primary_key=True)
    # data murid
    nik_murid = db.Column(db.String(16))
    no_kartu_keluarga = db.Column(db.String(16))
    nama_murid = db.Column(db.String(200))
    jenis_kelamin_murid = db.Column(db.String(15))
    tempat_lahir_murid = db.Column(db.String(100))
    tanggal_lahir_murid = db.Column(db.String(15))
    nama_ibu_kandung_murid = db.Column(db.String(200))
    kelas = db.Column(db.String(2))
    nisn_murid = db.Column(db.String(10))
    masa_berlaku_identitas = db.Column(db.String(100))
    no_hp_murid = db.Column(db.String(12))
    no_telepon = db.Column(db.String(100))
    alamat_surat = db.Column(db.String(20))
    tipe_alamat = db.Column(db.String(40))
    status_tempat_tinggal = db.Column(db.String(30))
    agama_murid = db.Column(db.String(20))
    pendidikan = db.Column(db.String(3))
    untuk_disabilitas = db.Column(db.String(30))

    # === DATA MURID (tambahan) ===
    alamat_murid = db.Column(db.String(300))
    rt_murid = db.Column(db.String(5))
    rw_murid = db.Column(db.String(5))
    provinsi_murid = db.Column(db.String(100))
    kota_murid = db.Column(db.String(100))
    kecamatan_murid = db.Column(db.String(100))
    kelurahan_murid = db.Column(db.String(100))
    kode_pos_murid = db.Column(db.String(10))
    npwp_murid = db.Column(db.String(30))

    # === DATA WALI ===
    nama_wali = db.Column(db.String(200))
    no_ktp_wali = db.Column(db.String(16))
    masa_berlaku_ktp_wali = db.Column(db.String(100))
    npwp_wali = db.Column(db.String(30))
    kartu_keluarga_wali = db.Column(db.String(16))
    tempat_lahir_wali = db.Column(db.String(100))
    tanggal_lahir_wali = db.Column(db.String(15))
    jenis_kelamin_wali = db.Column(db.String(15))
    agama_wali = db.Column(db.String(20))
    nama_ibu_kandung_wali = db.Column(db.String(200))
    pekerjaan_wali = db.Column(db.String(50))
    status_pernikahan_wali = db.Column(db.String(20))
    pendidikan_wali = db.Column(db.String(5))
    jabatan_wali = db.Column(db.String(20))
    alamat_wali = db.Column(db.String(300))
    rt_wali = db.Column(db.String(5))
    rw_wali = db.Column(db.String(5))
    provinsi_wali = db.Column(db.String(100))
    kota_wali = db.Column(db.String(100))
    kecamatan_wali = db.Column(db.String(100))
    kelurahan_wali = db.Column(db.String(100))
    kode_pos_wali = db.Column(db.String(10))
    status_tempat_tinggal_wali = db.Column(db.String(30))
    no_hp_wali = db.Column(db.String(15))
    no_telepon_wali = db.Column(db.String(15))
    tipe_alamat_wali = db.Column(db.String(40))

    # === KONTAK DARURAT ===
    nama_kontak_darurat = db.Column(db.String(200))
    no_identitas_kontak = db.Column(db.String(16))
    hubungan_kontak = db.Column(db.String(50))
    alamat_kontak = db.Column(db.String(300))
    rt_kontak = db.Column(db.String(5))
    rw_kontak = db.Column(db.String(5))
    provinsi_kontak = db.Column(db.String(100))
    kota_kontak = db.Column(db.String(100))
    kecamatan_kontak = db.Column(db.String(100))
    kelurahan_kontak = db.Column(db.String(100))
    kode_pos_kontak = db.Column(db.String(10))
    no_telepon_kontak = db.Column(db.String(15))

    # === SURAT PERMOHONAN ===
    nama_pemohon = db.Column(db.String(200))
    alamat_pemohon = db.Column(db.String(300))
    rt_pemohon = db.Column(db.String(5))
    rw_pemohon = db.Column(db.String(5))
    kelurahan_pemohon = db.Column(db.String(100))
    kecamatan_pemohon = db.Column(db.String(100))
    kota_pemohon = db.Column(db.String(100))
    kode_pos_pemohon = db.Column(db.String(10))
    telepon_pemohon = db.Column(db.String(15))
    nama_sekolah = db.Column(db.String(200))
    alamat_sekolah = db.Column(db.String(300))
    rt_sekolah = db.Column(db.String(5))
    rw_sekolah = db.Column(db.String(5))
    kelurahan_sekolah = db.Column(db.String(100))
    kecamatan_sekolah = db.Column(db.String(100))
    kota_sekolah = db.Column(db.String(100))
    kode_pos_sekolah = db.Column(db.String(10))
    ttd_pemohon = db.Column(db.Text)   # base64 PNG

    # === SURAT PERNYATAAN ===
    sp_nama_peserta = db.Column(db.String(200))
    sp_sekolah = db.Column(db.String(200))
    sp_kelas = db.Column(db.String(2))
    sp_nama_ortu = db.Column(db.String(200))
    sp_alamat_rumah = db.Column(db.String(300))
    ttd_ortu = db.Column(db.Text)   # base64 PNG
    ttd_penerima = db.Column(db.Text)   # base64 PNG
    sptm_nama = db.Column(db.String(200))
    sptm_noktp = db.Column(db.String(16))
    sptm_pekerjaan = db.Column(db.String(100))
    sptm_alamat = db.Column(db.String(300))
    ttd_sptm = db.Column(db.Text)   # base64 PNG

    # === BERITA ACARA ===
    ba_nama_penilai = db.Column(db.String(200))
    ba_jabatan_penilai = db.Column(db.String(100))
    ba_nama_siswa = db.Column(db.String(200))
    ba_nik_siswa = db.Column(db.String(16))
    ba_kelas = db.Column(db.String(2))
    penilaian_1 = db.Column(db.String(5))
    penilaian_2 = db.Column(db.String(5))
    penilaian_3 = db.Column(db.String(5))
    penilaian_4 = db.Column(db.String(5))
    ttd_ba_siswa = db.Column(db.Text)  
    ttd_ba_penilai = db.Column(db.Text)


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
