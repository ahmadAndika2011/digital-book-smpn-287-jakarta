"""
fill_kjp_pdf.py
===============
Script untuk mengisi Formulir KJP Plus dari data database.
Kolom database yang didukung: id, tanggal, nama, no_telepon, keterangan

Cara pakai di Flask:
    from fill_kjp_pdf import fill_kjp_pdf
    pdf_bytes = fill_kjp_pdf(siswa_dict)
    # siswa_dict contoh:
    # {
    #     "nama": "Budi Santoso",
    #     "no_telepon": "08123456789",
    #     "keterangan": "Catatan tambahan",
    #     "tanggal": "2026-01-15"
    # }
"""

import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import copy
import os
from reportlab.lib.utils import ImageReader


# ─────────────────────────────────────────
# Koordinat field dalam PDF (satuan: points)
# Sistem koordinat PDF: y=0 di BAWAH halaman
# PDF size: w=595.44, h=841.92
# ─────────────────────────────────────────

PDF_W = 595.44
PDF_H = 842


def top_to_pdf_y(top, h=PDF_H):
    """Konversi koordinat 'top' (y dari atas) ke koordinat PDF (y dari bawah)."""
    # return h - top
    return h - top

def top_to_pdf_y_for_folio(top):
    return 936.00 - top


# Field definitions: (page_index, x, pdf_y, max_width, font_size) * 0.479
# page_index = 0-based (page 0 = halaman 1, page 1 = halaman 2, dst)
FIELDS_DATA_SISWA = {
    # ? data murid
    "nama_murid": {
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(182),
        "max_w": 170,
        "font_size": 9,
    },
    "tempat_lahir_murid": {
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(212),
        "max_w": 170,
        "font_size": 9,
    },
    "nik_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(150),
        "max_w": 170,
        "font_size": 9,
    },
    "no_kartu_keluarga":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(165),
        "max_w": 170,
        "font_size": 9,
    },
    "jenis_kelamin_murid":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tanggal_1":{
        "page": 1,
        "x": 233,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tanggal_2":{
        "page": 1,
        "x": 255,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_bulan_1":{
        "page": 1,
        "x": 287,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_bulan_2":{
        "page": 1,
        "x": 306,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tahun_1":{
        "page": 1,
        "x": 340,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tahun_2":{
        "page": 1,
        "x": 356,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tahun_3":{
        "page": 1,
        "x": 374,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_murid_tahun_4":{
        "page": 1,
        "x": 394,
        "y": top_to_pdf_y(231),
        "max_w": 170,
        "font_size": 9,
    },
    "nama_ibu_kandung_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(243),
        "max_w": 170,
        "font_size": 9,
    },
    "kelas":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "nisn_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(407),
        "max_w": 170,
        "font_size": 9,
    },
    "masa_berlaku_identitas":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "no_hp_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(452),
        "max_w": 170,
        "font_size": 9,
    },
    "no_telepon":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(468),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_surat":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "tipe_alamat":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "status_tempat_tinggal":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "agama_murid":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "untuk_disabilitas":{
        "page": 1,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "pendidikan":{
        "page": 1,
        "x": 236,
        "y": top_to_pdf_y(632),
        "max_w": 170,
        "font_size": 9,
    },
    "npwp_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(423),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(261),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_murid":{
        "page": 1,
        "x": 231,
        "y": top_to_pdf_y(280),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_murid":{
        "page": 1,
        "x": 274,
        "y": top_to_pdf_y(280),
        "max_w": 170,
        "font_size": 9,
    },
    "provinsi_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(291),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(306),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(320),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(337),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_murid":{
        "page": 1,
        "x": 222,
        "y": top_to_pdf_y(352),
        "max_w": 170,
        "font_size": 9,
    },

    # ? data wali
    "nama_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(100),
        "max_w": 170,
        "font_size": 9,
    },
    "no_ktp_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(114),
        "max_w": 170,
        "font_size": 9,
    },
    "masa_berlaku_ktp_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(130),
        "max_w": 170,
        "font_size": 9,
    },
    "npwp_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(146),
        "max_w": 170,
        "font_size": 9,
    },
    "kartu_keluarga_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(161),
        "max_w": 170,
        "font_size": 9,
    },
    "tempat_lahir_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(177),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tanggal_1":{
        "page": 2,
        "x": 239,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tanggal_2":{
        "page": 2,
        "x": 260,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_bulan_1":{
        "page": 2,
        "x": 293,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_bulan_2":{
        "page": 2,
        "x": 315,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tahun_1":{
        "page": 2,
        "x": 345,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tahun_2":{
        "page": 2,
        "x": 364,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tahun_3":{
        "page": 2,
        "x": 381,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "tanggal_lahir_wali_tahun_4":{
        "page": 2,
        "x": 399,
        "y": top_to_pdf_y(196),
        "max_w": 170,
        "font_size": 9,
    },
    "jenis_kelamin_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "agama_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "nama_ibu_kandung_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(322),
        "max_w": 170,
        "font_size": 9,
    },
    "pekerjaan_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "status_pernikahan_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "pendidikan_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "jabatan_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(444),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_wali":{
        "page": 2,
        "x": 232,
        "y": top_to_pdf_y(462),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_wali":{
        "page": 2,
        "x": 270,
        "y": top_to_pdf_y(462),
        "max_w": 170,
        "font_size": 9,
    },
    "provinsi_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(475),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(490),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(506),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(521),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(536),
        "max_w": 170,
        "font_size": 9,
    },
    "status_tempat_tinggal_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "no_hp_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(567),
        "max_w": 170,
        "font_size": 9,
    },
    "no_telepon_wali":{
        "page": 2,
        "x": 222,
        "y": top_to_pdf_y(583),
        "max_w": 170,
        "font_size": 9,
    },
    "tipe_alamat_wali":{
        "page": 2,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },

    # ? data kontak darurat
    "nama_kontak_darurat":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(101),
        "max_w": 170,
        "font_size": 9,
    },
    "no_identitas_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(129),
        "max_w": 170,
        "font_size": 9,
    },
    "hubungan_kontak":{
        "page": 3,
        "x": 0,
        "y": top_to_pdf_y(0),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(204),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_kontak":{
        "page": 3,
        "x": 232,
        "y": top_to_pdf_y(223),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_kontak":{
        "page": 3,
        "x": 268,
        "y": top_to_pdf_y(223),
        "max_w": 170,
        "font_size": 9,
    },
    "provinsi_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(235),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(250),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(266),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(281),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(297),
        "max_w": 170,
        "font_size": 9,
    },
    "no_telepon_kontak":{
        "page": 3,
        "x": 222,
        "y": top_to_pdf_y(312),
        "max_w": 170,
        "font_size": 9,
    },

    # ? data permohonan
    "nama_pemohon": {
        "page": 4,
        "x": 276, 
        "y": top_to_pdf_y_for_folio(233), 
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(249),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(264),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_pemohon": {
        "page": 4,
        "x": 290,
        "y": top_to_pdf_y_for_folio(264),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(281),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(296),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_pemohon": {
        "page": 4,
        "x": 309,
        "y": top_to_pdf_y_for_folio(313),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_pemohon": {
        "page": 4,
        "x": 466,
        "y": top_to_pdf_y_for_folio(313),
        "max_w": 170,
        "font_size": 9,
    },
    "telepon_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(328),
        "max_w": 170,
        "font_size": 9,
    },
    "nama_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(408),
        "max_w": 170,
        "font_size": 9,
    },
    "tempat_tanggal_lahir_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(425),
        "max_w": 170,
        "font_size": 9,
    },
    "jenis_kelamin_peserta_didik_pemohon": {
        "page": 4,
        "x": 0,
        "y": top_to_pdf_y_for_folio(442),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(456),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(472),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_peserta_didik_pemohon": {
        "page": 4,
        "x": 290,
        "y": top_to_pdf_y_for_folio(472),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(488),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_peserta_didik_pemohon": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(503),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_peserta_didik_pemohon": {
        "page": 4,
        "x": 309,
        "y": top_to_pdf_y_for_folio(519),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_peserta_didik_pemohon": {
        "page": 4,
        "x": 466,
        "y": top_to_pdf_y_for_folio(519),
        "max_w": 170,
        "font_size": 9,
    },
    "nama_sekolah": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(536),
        "max_w": 170,
        "font_size": 9,
    },
    "alamat_sekolah": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(551),
        "max_w": 170,
        "font_size": 9,
    },
    "rt_sekolah": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(568),
        "max_w": 170,
        "font_size": 9,
    },
    "rw_sekolah": {
        "page": 4,
        "x": 290,
        "y": top_to_pdf_y_for_folio(568),
        "max_w": 170,
        "font_size": 9,
    },
    "kelurahan_sekolah": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(582),
        "max_w": 170,
        "font_size": 9,
    },
    "kecamatan_sekolah": {
        "page": 4,
        "x": 276,
        "y": top_to_pdf_y_for_folio(599),
        "max_w": 170,
        "font_size": 9,
    },
    "kota_sekolah": {
        "page": 4,
        "x": 309,
        "y": top_to_pdf_y_for_folio(614),
        "max_w": 170,
        "font_size": 9,
    },
    "kode_pos_sekolah": {
        "page": 4,
        "x": 466,
        "y": top_to_pdf_y_for_folio(614),
        "max_w": 170,
        "font_size": 9,
    },
    "ttd_pemohon": {
        "page": 4,
        "x": 390,
        "y": top_to_pdf_y_for_folio(870),
        "max_w": 170,
        "font_size": 9,
        "img_w": 100,  
        "img_h": 50,  
    },
}


def _make_overlay(page_fields, page_w, page_h):
    """Buat overlay PDF transparan berisi teks/gambar untuk satu halaman."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_w, page_h))

    # Field yang berisi gambar (bukan teks)
    IMAGE_FIELDS = {"ttd_pemohon", "ttd_sekolah"}  # tambah lainnya jika ada

    for field_name, value, cfg in page_fields:
        font_size = cfg.get("font_size", 10)

        if field_name in IMAGE_FIELDS:
            # ── Gambar PNG (tanda tangan) ──
            if value and os.path.exists(value):
                try:
                    img = ImageReader(value)
                    img_w = cfg.get("img_w", 80)   # lebar gambar di PDF
                    img_h = cfg.get("img_h", 40)   # tinggi gambar di PDF
                    c.drawImage(
                        img,
                        cfg["x"],
                        cfg["y"],
                        width=img_w,
                        height=img_h,
                        mask="auto",  # transparan (support PNG)
                        preserveAspectRatio=True,
                    )
                except Exception as e:
                    print(f"[WARNING] Gagal load gambar {field_name}: {e}")
        else:
            # ── Teks biasa ──
            c.setFillColor(colors.black)
            c.setFont("Helvetica", font_size)
            text = str(value)
            while text and c.stringWidth(text, "Helvetica", font_size) > cfg["max_w"]:
                text = text[:-1]
            c.drawString(cfg["x"], cfg["y"], text)

    c.save()
    packet.seek(0)
    return PdfReader(packet)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_upload_path(filename: str) -> str:
    return os.path.join(BASE_DIR, "..", "static", "uploads", "ttd", filename)

def fill_kjp_pdf(siswa: dict, template_path: str = "formulir_kjp.pdf") -> bytes:
    """
        data Murid
    """
    nama_murid  = siswa.get("nama_murid", "")
    tempat_lahir_murid  = siswa.get("tempat_lahir_murid", "")
    jenis_kelamin_murid = siswa.get("jenis_kelamin_murid", "")
    nik_murid = siswa.get("nik_murid", "")
    no_kartu_keluarga = siswa.get("no_kartu_keluarga", "")
    tanggal_lahir_murid = siswa.get("tanggal_lahir_murid", "")
    nama_ibu_kandung_murid = siswa.get("nama_ibu_kandung_murid", "")
    kelas = siswa.get("kelas", "")
    nisn_murid = siswa.get("nisn_murid", "")
    masa_berlaku_identitas = siswa.get("masa_berlaku_identitas", "")
    no_hp_murid = siswa.get("no_hp_murid", "")
    no_telepon = siswa.get("no_telepon", "")
    alamat_surat = siswa.get("alamat_surat", "")
    tipe_alamat = siswa.get("tipe_alamat", "")
    status_tempat_tinggal = siswa.get("status_tempat_tinggal", "")
    agama_murid = siswa.get("agama_murid", "")
    untuk_disabilitas = siswa.get("untuk_disabilitas", "")
    npwp_murid = siswa.get("npwp_murid", "")
    alamat_murid = siswa.get("alamat_murid", "")
    rt_murid = siswa.get("rt_murid", "")
    rw_murid = siswa.get("rw_murid", "")
    provinsi_murid = siswa.get("provinsi_murid", "")
    kota_murid = siswa.get("kota_murid", "")
    kecamatan_murid = siswa.get("kecamatan_murid", "")
    kelurahan_murid = siswa.get("kelurahan_murid", "")
    kode_pos_murid = siswa.get("kode_pos_murid", "")

    # # Cek Jenis Kelamin
    if jenis_kelamin_murid == "Laki-laki":
        FIELDS_DATA_SISWA["jenis_kelamin_murid"]["x"] = 234
        FIELDS_DATA_SISWA["jenis_kelamin_murid"]["y"] = top_to_pdf_y(200)
    else:
        FIELDS_DATA_SISWA["jenis_kelamin_murid"]["x"] = 313
        FIELDS_DATA_SISWA["jenis_kelamin_murid"]["y"] = top_to_pdf_y(200)

    # # Cek kelas
    if kelas == "7":
        FIELDS_DATA_SISWA["kelas"]["x"] = 388
        FIELDS_DATA_SISWA["kelas"]["y"] = top_to_pdf_y(371)
    elif kelas == "8":
        FIELDS_DATA_SISWA["kelas"]["x"] = 388
        FIELDS_DATA_SISWA["kelas"]["y"] = top_to_pdf_y(384)
    elif kelas == "9":
        FIELDS_DATA_SISWA["kelas"]["x"] = 388
        FIELDS_DATA_SISWA["kelas"]["y"] = top_to_pdf_y(396)
    else:
        FIELDS_DATA_SISWA["kelas"]["x"] = 0
        FIELDS_DATA_SISWA["kelas"]["y"] = top_to_pdf_y(0)

    # # Cek Masa Berlaku Identitas
    if masa_berlaku_identitas == "Seumur Hidup":
        FIELDS_DATA_SISWA["masa_berlaku_identitas"]["x"] = 307
        FIELDS_DATA_SISWA["masa_berlaku_identitas"]["y"] = top_to_pdf_y(440)
    else:
        FIELDS_DATA_SISWA["masa_berlaku_identitas"]["x"] = 222
        FIELDS_DATA_SISWA["masa_berlaku_identitas"]["y"] = top_to_pdf_y(437)

    # # Cek Alamat Surat
    if alamat_surat == "Diambil Sendiri":
        FIELDS_DATA_SISWA["alamat_surat"]["x"] = 236
        FIELDS_DATA_SISWA["alamat_surat"]["y"] = top_to_pdf_y(487)
    elif alamat_surat == "Dikirim":
        FIELDS_DATA_SISWA["alamat_surat"]["x"] = 344
        FIELDS_DATA_SISWA["alamat_surat"]["y"] = top_to_pdf_y(487)

    # # Cek Tipe Alamat
    if tipe_alamat == "Alamat Rumah":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 236
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(508)
    elif tipe_alamat == "Alamat Kantor":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 236
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(520)
    elif tipe_alamat == "Alamat Kost":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 236
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(533)
    elif tipe_alamat == "Alamat Sesuai KK":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 236
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(546)
    elif tipe_alamat == "Alamat Sesuai NPWP":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 344
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(508)
    elif tipe_alamat == "Alamat Rusun":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 344
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(519)
    elif tipe_alamat == "Alamat Panti":
        FIELDS_DATA_SISWA["tipe_alamat"]["x"] = 344
        FIELDS_DATA_SISWA["tipe_alamat"]["y"] = top_to_pdf_y(534)

    # # Cek Status Tempat Tinggal
    if status_tempat_tinggal == "Bukan Milik Pribadi":
        FIELDS_DATA_SISWA["status_tempat_tinggal"]["x"] = 237
        FIELDS_DATA_SISWA["status_tempat_tinggal"]["y"] = top_to_pdf_y(560)
    elif status_tempat_tinggal == "Milik Pribadi":
        FIELDS_DATA_SISWA["status_tempat_tinggal"]["x"] = 392
        FIELDS_DATA_SISWA["status_tempat_tinggal"]["y"] = top_to_pdf_y(560)

    # # Cek Agama Murid
    if agama_murid == "Islam":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 310
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(596)
    if agama_murid == "Protestan":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 310
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Katolik":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 391
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Hindu":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 237
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Budha":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 237
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(596)
    if agama_murid == "Lainnya":
        FIELDS_DATA_SISWA["agama_murid"]["x"] = 391
        FIELDS_DATA_SISWA["agama_murid"]["y"] = top_to_pdf_y(596)

    # # Cek untuk Disabilitas
    if untuk_disabilitas == "Tidak Ada":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 0
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(0)
    elif untuk_disabilitas == "Tuna Rungu":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(664)
    elif untuk_disabilitas == "Tuna Netra":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(676)
    elif untuk_disabilitas == "Tuna Wicara":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(690)
    elif untuk_disabilitas == "Tuna Daksa":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(703)
    elif untuk_disabilitas == "Tuna Grahita":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(716)
    elif untuk_disabilitas == "Tuna Laras":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(729)
    elif untuk_disabilitas == "Tuna Ganda":
        FIELDS_DATA_SISWA["untuk_disabilitas"]["x"] = 237
        FIELDS_DATA_SISWA["untuk_disabilitas"]["y"] = top_to_pdf_y(743)

    """
        data Wali
    """
    nama_wali = siswa.get("nama_wali", "")
    no_ktp_wali = siswa.get("no_ktp_wali", "")
    masa_berlaku_ktp_wali = siswa.get("masa_berlaku_ktp_wali", "")
    npwp_wali = siswa.get("npwp_wali", "")
    kartu_keluarga_wali = siswa.get("kartu_keluarga_wali", "")
    tempat_lahir_wali = siswa.get("tempat_lahir_wali", "")
    tanggal_lahir_wali = siswa.get("tanggal_lahir_wali", "")
    jenis_kelamin_wali = siswa.get("jenis_kelamin_wali", "")
    agama_wali = siswa.get("agama_wali", "")
    nama_ibu_kandung_wali = siswa.get("nama_ibu_kandung_wali", "")
    pekerjaan_wali = siswa.get("pekerjaan_wali", "")
    status_pernikahan_wali = siswa.get("status_pernikahan_wali", "")
    pendidikan_wali = siswa.get("pendidikan_wali", "")
    jabatan_wali = siswa.get("jabatan_wali", "")
    alamat_wali = siswa.get("alamat_wali", "")
    rt_wali = siswa.get("rt_wali", "")
    rw_wali = siswa.get("rw_wali", "")
    provinsi_wali = siswa.get("provinsi_wali", "")
    kota_wali = siswa.get("kota_wali", "")
    kecamatan_wali = siswa.get("kecamatan_wali", "")
    kelurahan_wali = siswa.get("kelurahan_wali", "")
    kode_pos_wali = siswa.get("kode_pos_wali", "")
    status_tempat_tinggal_wali = siswa.get("status_tempat_tinggal_wali", "")
    no_hp_wali = siswa.get("no_hp_wali", "")
    no_telepon_wali = siswa.get("no_telepon_wali", "")
    tipe_alamat_wali = siswa.get("tipe_alamat_wali", "")

    # # cek masa berlaku ktp wali
    if masa_berlaku_ktp_wali == "Seumur Hidup":
        FIELDS_DATA_SISWA["masa_berlaku_ktp_wali"]["x"] = 311
        FIELDS_DATA_SISWA["masa_berlaku_ktp_wali"]["y"] = top_to_pdf_y(131)

    # # cek jenis kelamin wali
    if jenis_kelamin_wali == "Laki-laki":
        FIELDS_DATA_SISWA["jenis_kelamin_wali"]["x"] = 239
        FIELDS_DATA_SISWA["jenis_kelamin_wali"]["y"] = top_to_pdf_y(214)
    elif jenis_kelamin_wali == "Perempuan":
        FIELDS_DATA_SISWA["jenis_kelamin_wali"]["x"] = 317
        FIELDS_DATA_SISWA["jenis_kelamin_wali"]["y"] = top_to_pdf_y(214)

    # # cek agama wali
    if agama_wali == "Hindu":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 239
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(239)
    elif agama_wali == "Protestan":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 315
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(239)
    elif agama_wali == "Katolik":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 394
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(239)
    elif agama_wali == "Budha":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 239
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(248)
    elif agama_wali == "Islam":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 315
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(248)
    elif agama_wali == "Lainnya":
        FIELDS_DATA_SISWA["agama_wali"]["x"] = 394
        FIELDS_DATA_SISWA["agama_wali"]["y"] = top_to_pdf_y(248)

    # # cek pekerjaan wali
    if pekerjaan_wali == "Pelajar/Mahasiswa":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(266)
    elif pekerjaan_wali == "Ibu Rumah Tangga":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 348
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(266)
    elif pekerjaan_wali == "Pegawai Swasta":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(279)
    elif pekerjaan_wali == "Wiraswasta":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 348
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(279)
    elif pekerjaan_wali == "TNI/Polri":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(293)
    elif pekerjaan_wali == "Pensiunan":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 348
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(293)
    elif pekerjaan_wali == "Pegawai Negeri":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(307)
    elif pekerjaan_wali == "Lain-Lain":
        FIELDS_DATA_SISWA["pekerjaan_wali"]["x"] = 348
        FIELDS_DATA_SISWA["pekerjaan_wali"]["y"] = top_to_pdf_y(307)

    # # cek nama ibu kandung wali
    if status_pernikahan_wali == "Lajang":
        FIELDS_DATA_SISWA['status_pernikahan_wali']["x"] = 239
        FIELDS_DATA_SISWA['status_pernikahan_wali']["y"] = top_to_pdf_y(344)
    elif status_pernikahan_wali == "Menikah":
        FIELDS_DATA_SISWA['status_pernikahan_wali']["x"] = 313
        FIELDS_DATA_SISWA['status_pernikahan_wali']["y"] = top_to_pdf_y(344)
    elif status_pernikahan_wali == "Janda/Duda":
        FIELDS_DATA_SISWA['status_pernikahan_wali']["x"] = 383
        FIELDS_DATA_SISWA['status_pernikahan_wali']["y"] = top_to_pdf_y(344)

    # # cek pendidikan wali
    if pendidikan_wali == "SD":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(367)
    elif pendidikan_wali == "SMP":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(380)
    elif pendidikan_wali == "SMA":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 239
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(393)
    elif pendidikan_wali == "D1":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 313
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(367)
    elif pendidikan_wali == "D2":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 313
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(380)
    elif pendidikan_wali == "D3":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 313
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(393)
    elif pendidikan_wali == "S1":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 384
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(367)
    elif pendidikan_wali == "S2":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 384
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(380)
    elif pendidikan_wali == "S3":
        FIELDS_DATA_SISWA["pendidikan_wali"]["x"] = 384
        FIELDS_DATA_SISWA["pendidikan_wali"]["y"] = top_to_pdf_y(393)

    # # cek jabatan wali
    if jabatan_wali == "Tetap":
        FIELDS_DATA_SISWA["jabatan_wali"]["x"] = 238
        FIELDS_DATA_SISWA["jabatan_wali"]["y"] = top_to_pdf_y(418)
    elif jabatan_wali == "Honorer":
        FIELDS_DATA_SISWA["jabatan_wali"]["x"] = 314
        FIELDS_DATA_SISWA["jabatan_wali"]["y"] = top_to_pdf_y(418)
    elif jabatan_wali == "kontrak":
        FIELDS_DATA_SISWA["jabatan_wali"]["x"] = 238
        FIELDS_DATA_SISWA["jabatan_wali"]["y"] = top_to_pdf_y(430)
    elif jabatan_wali == "Tidak Kerja":
        FIELDS_DATA_SISWA["jabatan_wali"]["x"] = 314
        FIELDS_DATA_SISWA["jabatan_wali"]["y"] = top_to_pdf_y(430)

    # # cek status tempat tinggal
    if status_tempat_tinggal_wali == "Bukan Milik Pribadi":
        FIELDS_DATA_SISWA["status_tempat_tinggal_wali"]["x"] = 240
        FIELDS_DATA_SISWA["status_tempat_tinggal_wali"]["y"] = top_to_pdf_y(555)
    elif status_tempat_tinggal_wali == "Milik Pribadi":
        FIELDS_DATA_SISWA["status_tempat_tinggal_wali"]["x"] = 386
        FIELDS_DATA_SISWA["status_tempat_tinggal_wali"]["y"] = top_to_pdf_y(555)

    # # cek tipe tempat tinggal
    if tipe_alamat_wali == "Alamat Rumah":
        FIELDS_DATA_SISWA["tipe_alamat_wali"]["x"] = 239
        FIELDS_DATA_SISWA["tipe_alamat_wali"]["y"] = top_to_pdf_y(600)
    elif tipe_alamat_wali == "Alamat Kost":
        FIELDS_DATA_SISWA["tipe_alamat_wali"]["x"] = 347
        FIELDS_DATA_SISWA["tipe_alamat_wali"]["y"] = top_to_pdf_y(600)

    # """
    #     Data Kontak Darurat
    # """
    nama_kontak_darurat = siswa.get("nama_kontak_darurat", "")
    no_identitas_kontak = siswa.get("no_identitas_kontak", "")
    alamat_kontak = siswa.get("alamat_kontak", "")
    provinsi_kontak = siswa.get("provinsi_kontak", "")
    kota_kontak = siswa.get("kota_kontak", "")
    kecamatan_kontak = siswa.get("kecamatan_kontak", "")
    kelurahan_kontak = siswa.get("kelurahan_kontak", "")
    kode_pos_kontak = siswa.get("kode_pos_kontak", "")
    no_telepon_kontak = siswa.get("no_telepon_kontak", "")
    hubungan_kontak = siswa.get("hubungan_kontak", "")
    rt_kontak = siswa.get("rt_kontak", "")
    rw_kontak = siswa.get("rw_kontak", "")

    # # cek hubungan kontak
    if hubungan_kontak == "Orangtua Kandung/Tiri/Angkat":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 226
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(146)
    elif hubungan_kontak == "Ipar dari Istri/Suami":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 393
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(146)
    elif hubungan_kontak == "Saudara Kandung/Tiiri/Angkat":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 226
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(159)
    elif hubungan_kontak == "AnakKandung/Tiri/Angkat":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 393
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(159)
    elif hubungan_kontak == "Suami/Istri":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 226
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(172)
    elif hubungan_kontak == "Mertua":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 393
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(172)
    elif hubungan_kontak == "Kakek/Nenek":
        FIELDS_DATA_SISWA["hubungan_kontak"]["x"] = 226
        FIELDS_DATA_SISWA["hubungan_kontak"]["y"] = top_to_pdf_y(186)

    """
        data permohonan
    """
    nama_pemohon = siswa.get("nama_pemohon", "")
    alamat_pemohon = siswa.get("alamat_pemohon", "")
    rt_pemohon = siswa.get("rt_pemohon", "")
    rw_pemohon = siswa.get("rw_pemohon", "")
    kelurahan_pemohon = siswa.get("kelurahan_pemohon", "")
    kecamatan_pemohon = siswa.get("kecamatan_pemohon", "")
    kota_pemohon = siswa.get("kota_pemohon", "")
    kode_pos_pemohon = siswa.get("kode_pos_pemohon", "")
    telepon_pemohon = siswa.get("telepon_pemohon", "")
    nama_sekolah = siswa.get("nama_sekolah", "")
    alamat_sekolah = siswa.get("alamat_sekolah", "")
    rt_sekolah = siswa.get("rt_sekolah", "")
    rw_sekolah = siswa.get("rw_sekolah", "")
    kelurahan_sekolah = siswa.get("kelurahan_sekolah", "")
    kecamatan_sekolah = siswa.get("kecamatan_sekolah", "")
    kota_sekolah = siswa.get("kota_sekolah", "")
    kode_pos_sekolah = siswa.get("kode_pos_sekolah", "")
    ttd_pemohon = siswa.get("ttd_pemohon", "")

    if jenis_kelamin_murid == "Laki-laki":
        FIELDS_DATA_SISWA["jenis_kelamin_peserta_didik_pemohon"]["x"] = 280
    elif jenis_kelamin_murid == "Perempuan":
        FIELDS_DATA_SISWA["jenis_kelamin_peserta_didik_pemohon"]["x"] = 333

    # Kelompokkan field berdasarkan halaman
    page_data = {}

    field_map = [
        # ? data siswa
        ("nama_murid",     nama_murid),
        ("tempat_lahir_murid", tempat_lahir_murid),
        ("nik_murid", nik_murid),
        ("no_kartu_keluarga", no_kartu_keluarga),
        ("jenis_kelamin_murid", "✓"),
        ("tanggal_lahir_murid_tanggal_1", tanggal_lahir_murid.split("-")[2][0]),
        ("tanggal_lahir_murid_tanggal_2", tanggal_lahir_murid.split("-")[2][1]),
        ("tanggal_lahir_murid_bulan_1", tanggal_lahir_murid.split("-")[1][0]),
        ("tanggal_lahir_murid_bulan_2", tanggal_lahir_murid.split("-")[1][1]),
        ("tanggal_lahir_murid_tahun_1", tanggal_lahir_murid.split("-")[0][0]),
        ("tanggal_lahir_murid_tahun_2", tanggal_lahir_murid.split("-")[0][1]),
        ("tanggal_lahir_murid_tahun_3", tanggal_lahir_murid.split("-")[0][2]),
        ("tanggal_lahir_murid_tahun_4", tanggal_lahir_murid.split("-")[0][3]),
        ("nama_ibu_kandung_murid", nama_ibu_kandung_murid),
        ("kelas", "✓"),
        ("nisn_murid", nisn_murid),
        ("masa_berlaku_identitas", "✓" if masa_berlaku_identitas == "Seumur Hidup" else masa_berlaku_identitas),
        ("no_hp_murid", no_hp_murid),
        ("no_telepon", no_telepon),
        ("alamat_surat", "✓"),
        ("tipe_alamat", "✓"),
        ("status_tempat_tinggal", "✓"),
        ("agama_murid", "✓"),
        ("untuk_disabilitas", "" if untuk_disabilitas == "Tidak Ada" else "✓"),
        ("pendidikan", "✓"),
        ("npwp_murid", npwp_murid),
        ("alamat_murid", alamat_murid),
        ("rt_murid", rt_murid),
        ("rw_murid", rw_murid),
        ("provinsi_murid", provinsi_murid),
        ("kota_murid", kota_murid),
        ("kecamatan_murid", kecamatan_murid),
        ("kelurahan_murid", kelurahan_murid),
        ("kode_pos_murid", kode_pos_murid),

        # ? data wali
        ("nama_wali", nama_wali),
        ("no_ktp_wali", no_ktp_wali),
        ("masa_berlaku_ktp_wali", "✓" if masa_berlaku_ktp_wali == "Seumur Hidup" else masa_berlaku_ktp_wali),
        ("npwp_wali", npwp_wali),
        ("kartu_keluarga_wali", kartu_keluarga_wali),
        ("tempat_lahir_wali", tempat_lahir_wali),
        ("tanggal_lahir_wali_tanggal_1", tanggal_lahir_wali.split("-")[2][0]),
        ("tanggal_lahir_wali_tanggal_2", tanggal_lahir_wali.split("-")[2][1]),
        ("tanggal_lahir_wali_bulan_1", tanggal_lahir_wali.split("-")[1][0]),
        ("tanggal_lahir_wali_bulan_2", tanggal_lahir_wali.split("-")[1][1]),
        ("tanggal_lahir_wali_tahun_1", tanggal_lahir_wali.split("-")[0][0]),
        ("tanggal_lahir_wali_tahun_2", tanggal_lahir_wali.split("-")[0][1]),
        ("tanggal_lahir_wali_tahun_3", tanggal_lahir_wali.split("-")[0][2]),
        ("tanggal_lahir_wali_tahun_4", tanggal_lahir_wali.split("-")[0][3]),
        ("jenis_kelamin_wali", "✓"),
        ("agama_wali", "✓"),
        ("nama_ibu_kandung_wali", nama_ibu_kandung_wali),
        ("pekerjaan_wali", "✓"),
        ("status_pernikahan_wali", "✓"),
        ("pendidikan_wali", "✓"),
        ("jabatan_wali", "✓"),
        ("alamat_wali", alamat_wali),
        ("rt_wali", rt_wali),
        ("rw_wali", rw_wali),
        ("provinsi_wali", provinsi_wali),
        ("kota_wali", kota_wali),
        ("kecamatan_wali", kecamatan_wali),
        ("kelurahan_wali", kelurahan_wali),
        ("kode_pos_wali", kode_pos_wali),
        ("status_tempat_tinggal_wali", "✓"),
        ("no_hp_wali", no_hp_wali),
        ("no_telepon_wali", no_telepon_wali),
        ("tipe_alamat_wali", "✓"),

        # ? data kontak darurat
        ("nama_kontak_darurat", nama_kontak_darurat),
        ("alamat_kontak", alamat_kontak),
        ("no_identitas_kontak", no_identitas_kontak),
        ("provinsi_kontak", provinsi_kontak),
        ("kota_kontak", kota_kontak),
        ("kecamatan_kontak", kecamatan_kontak),
        ("kelurahan_kontak", kelurahan_kontak),
        ("kode_pos_kontak", kode_pos_kontak),
        ("no_telepon_kontak", no_telepon_kontak),
        ("hubungan_kontak", "✓"),
        ("rt_kontak", rt_kontak),
        ("rw_kontak", rw_kontak),
        
        # ? data permohonan
        ("nama_pemohon", nama_pemohon),
        ("alamat_pemohon", alamat_pemohon),
        ("rt_pemohon", f"{rt_pemohon} / "),
        ("rw_pemohon", rw_pemohon),
        ("kelurahan_pemohon", kelurahan_pemohon),
        ("kecamatan_pemohon", kecamatan_pemohon),
        ("kota_pemohon", kota_pemohon),
        ("kode_pos_pemohon", kode_pos_pemohon),
        ("telepon_pemohon", telepon_pemohon),
        ("nama_peserta_didik_pemohon", nama_murid),
        ("tempat_tanggal_lahir_peserta_didik_pemohon", f"{tempat_lahir_murid}, {tanggal_lahir_murid}"),
        ("jenis_kelamin_peserta_didik_pemohon", "==============="),
        ("alamat_peserta_didik_pemohon", alamat_murid),
        ("rt_peserta_didik_pemohon", rt_murid),
        ("rw_peserta_didik_pemohon", rw_murid),
        ("kelurahan_peserta_didik_pemohon", kelurahan_murid),
        ("kecamatan_peserta_didik_pemohon", kecamatan_murid),
        ("kota_peserta_didik_pemohon", kota_murid),
        ("kode_pos_peserta_didik_pemohon", kode_pos_murid),
        ("nama_sekolah", nama_sekolah),
        ("alamat_sekolah", alamat_sekolah),
        ("rt_sekolah", f"{rt_sekolah} / "),
        ("rw_sekolah", rw_sekolah),
        ("kelurahan_sekolah", kelurahan_sekolah),
        ("kecamatan_sekolah", kecamatan_sekolah),
        ("kota_sekolah", kota_sekolah),
        ("kode_pos_sekolah", kode_pos_sekolah),
        ("kode_pos_sekolah", kode_pos_sekolah),
        ("ttd_pemohon", get_upload_path(ttd_pemohon)),
    ]

    for field_key, value in field_map:
        cfg = FIELDS_DATA_SISWA[field_key]
        pg = cfg["page"]
        if pg not in page_data:
            page_data[pg] = []
        page_data[pg].append((field_key, value, cfg))

    # Baca template
    reader = PdfReader(template_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        page_w = float(page.mediabox.width)
        page_h = float(page.mediabox.height)

        if i in page_data:
            overlay_reader = _make_overlay(page_data[i], page_w, page_h)
            overlay_page = overlay_reader.pages[0]
            page.merge_page(overlay_page)

        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()


def fill_kjp_pdf_permohonan(siswa: dict, template_path: str = "formulir_kjp.pdf") -> bytes:
    """
        data permohonan
    """
    nama_pemohon = siswa.get("nama_pemohon", "")
    alamat_pemohon = siswa.get("alamat_pemohon", "")
    rt_pemohon = siswa.get("rt_pemohon", "")
    rw_pemohon = siswa.get("rw_pemohon", "")
    kelurahan_pemohon = siswa.get("kelurahan_pemohon", "")
    kecamatan_pemohon = siswa.get("kecamatan_pemohon", "")
    kota_pemohon = siswa.get("kota_pemohon", "")
    kode_pos_pemohon = siswa.get("kode_pos_pemohon", "")
    telepon_pemohon = siswa.get("telepon_pemohon", "")
    nama_sekolah = siswa.get("nama_sekolah", "")
    alamat_sekolah = siswa.get("alamat_sekolah", "")
    rt_sekolah = siswa.get("rt_sekolah", "")
    rw_sekolah = siswa.get("rw_sekolah", "")
    kelurahan_sekolah = siswa.get("kelurahan_sekolah", "")
    kecamatan_sekolah = siswa.get("kecamatan_sekolah", "")
    kota_sekolah = siswa.get("kota_sekolah", "")
    kode_pos_sekolah = siswa.get("kode_pos_sekolah", "")
    ttd_pemohon = siswa.get("ttd_pemohon", "")


    # Kelompokkan field berdasarkan halaman
    page_data = {}

    field_map = [
        # ? data permohonan
        ("nama_pemohon", nama_pemohon),
        ("alamat_pemohon", alamat_pemohon),
        ("rt_pemohon", f"{rt_pemohon} / "),
        ("rw_pemohon", rw_pemohon),
        ("kelurahan_pemohon", kelurahan_pemohon),
        ("kecamatan_pemohon", kecamatan_pemohon),
        ("kota_pemohon", kota_pemohon),
        ("kode_pos_pemohon", kode_pos_pemohon),
        ("telepon_pemohon", telepon_pemohon),
        ("nama_sekolah", nama_sekolah),
        ("alamat_sekolah", alamat_sekolah),
        ("rt_sekolah", f"{rt_sekolah} / "),
        ("rw_sekolah", rw_sekolah),
        ("kelurahan_sekolah", kelurahan_sekolah),
        ("kecamatan_sekolah", kecamatan_pemohon),
        ("kota_sekolah", kota_sekolah),
        ("kode_pos_sekolah", kode_pos_sekolah),
        # ("ttd_pemohon", f"/static/uploads/ttd/{ttd_pemohon}"),
        ("ttd_pemohon", get_upload_path(ttd_pemohon)),
    ]

    for field_key, value in field_map:
        cfg = FIELDS_DATA_SISWA[field_key]
        pg = cfg["page"]
        if pg not in page_data:
            page_data[pg] = []
        page_data[pg].append((field_key, value, cfg))

    # Baca template
    reader = PdfReader(template_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        page_w = float(page.mediabox.width)
        page_h = float(page.mediabox.height)

        if i in page_data:
            overlay_reader = _make_overlay(page_data[i], page_w, page_h)
            overlay_page = overlay_reader.pages[0]
            page.merge_page(overlay_page)

        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()
