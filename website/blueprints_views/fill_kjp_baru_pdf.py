import io
from flask import request
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import copy
import os
from reportlab.lib.utils import ImageReader

FIELDS_DATA_SISWA = {
    "tanggal_surat": {
        "page": 0,
        "x": 380,
        "y": 830,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_nama": {
        "page": 0,
        "x": 245,
        "y": 700,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_alamat": {
        "page": 0,
        "x": 245,
        "y": 688,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_rt_rw": {
        "page": 0,
        "x": 245,
        "y": 670,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_kelurahan": {
        "page": 0,
        "x": 245,
        "y": 660,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_kecamatan": {
        "page": 0,
        "x": 245,
        "y": 645,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_kota": {
        "page": 0,
        "x": 280,
        "y": 630,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_kode_pos": {
        "page": 0,
        "x": 480,
        "y": 630,
        "max_w": 170,
        "font_size": 9,
    },
    "pemohon_telpon": {
        "page": 0,
        "x": 245,
        "y": 615,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_nama": {
        "page": 0,
        "x": 290,
        "y": 518,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_tempat_tanggal_lahir": {
        "page": 0,
        "x": 290,
        "y": 500,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_jenis_kelamin": {
        "page": 0,
        "x": 0,
        "y": 486,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_alamat": {
        "page": 0,
        "x": 290,
        "y": 475,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_rt_rw": {
        "page": 0,
        "x": 290,
        "y": 460,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_kelurahan": {
        "page": 0,
        "x": 290,
        "y": 448,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_kecamatan": {
        "page": 0,
        "x": 290,
        "y": 433,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_kota": {
        "page": 0,
        "x": 320,
        "y": 420,
        "max_w": 170,
        "font_size": 9,
    },
    "peserta_didik_kode_pos": {
        "page": 0,
        "x": 500,
        "y": 420,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_nama": {
        "page": 0,
        "x": 290,
        "y": 405,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_alamat": {
        "page": 0,
        "x": 290,
        "y": 390,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_rt_rw": {
        "page": 0,
        "x": 290,
        "y": 375,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_kelurahan": {
        "page": 0,
        "x": 290,
        "y": 362,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_kecamatan": {
        "page": 0,
        "x": 290,
        "y": 348,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_kota": {
        "page": 0,
        "x": 320,
        "y": 335,
        "max_w": 170,
        "font_size": 9,
    },
    "sekolah_kode_pos": {
        "page": 0,
        "x": 500,
        "y": 335,
        "max_w": 170,
        "font_size": 9,
    },
    "ttd_nama_lengkap": {
        "page": 0,
        "x": 410,
        "y": 115,
        "max_w": 170,
        "font_size": 9,
    },
    "ttd_tanda_tangan": {
        "page": 0,
        "x": 430,
        "y": 130,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_nama_peserta_didik": {
        "page": 1,
        "x": 220,
        "y": 590,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_nisn": {
        "page": 1,
        "x": 220,
        "y": 570,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_kelas": {
        "page": 1,
        "x": 220,
        "y": 540,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_sekolah": {
        "page": 1,
        "x": 220,
        "y": 550,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_nama_orang_tua": {
        "page": 1,
        "x": 220,
        "y": 520,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_alamat": {
        "page": 1,
        "x": 220,
        "y": 510,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_ttd_orang_tua": {
        "page": 1,
        "x": 150,
        "y": 230,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_ttd_penerima": {
        "page": 1,
        "x": 420,
        "y": 230,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_ttd_orang_tua_text": {
        "page": 1,
        "x": 150,
        "y": 200,
        "max_w": 170,
        "font_size": 9,
    },
    "pernyataan_ttd_penerima_text": {
        "page": 1,
        "x": 420,
        "y": 200,
        "max_w": 170,
        "font_size": 9,
    },
}




def _make_overlay(page_fields, page_w, page_h):
    """Buat overlay PDF transparan berisi teks/gambar untuk satu halaman."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_w, page_h))

    # Field yang berisi gambar (bukan teks)
    IMAGE_FIELDS = {"ttd_tanda_tangan", "pernyataan_ttd_orang_tua", "pernyataan_ttd_penerima"}

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
    return os.path.join(BASE_DIR, "..", "static", "uploads", filename)

def fill_kjp_baru_pdf(siswa: dict, template_path: str = "formulir_kjp.pdf") -> bytes:
    tanggal_surat = siswa.get("tanggal_surat", "")
    pemohon_nama = siswa.get("pemohon_nama", "")
    pemohon_alamat = siswa.get("pemohon_alamat", "")
    pemohon_rt_rw = siswa.get("pemohon_rt_rw", "")
    pemohon_kelurahan = siswa.get("pemohon_kelurahan", "")
    pemohon_kecamatan = siswa.get("pemohon_kecamatan", "")
    pemohon_kota = siswa.get("pemohon_kota", "")
    pemohon_kode_pos = siswa.get("pemohon_kode_pos", "")
    pemohon_telpon = siswa.get("pemohon_telpon", "")
    peserta_didik_nama = siswa.get("peserta_didik_nama", "")
    peserta_didik_tempat_lahir = siswa.get("peserta_didik_tempat_lahir", "")
    peserta_didik_tanggal_lahir = siswa.get("peserta_didik_tanggal_lahir", "")
    peserta_didik_jenis_kelamin = siswa.get("peserta_didik_jenis_kelamin", "")
    peserta_didik_alamat = siswa.get("peserta_didik_alamat", "")
    peserta_didik_rt_rw = siswa.get("peserta_didik_rt_rw", "")
    peserta_didik_kelurahan = siswa.get("peserta_didik_kelurahan", "")
    peserta_didik_kecamatan = siswa.get("peserta_didik_kecamatan", "")
    peserta_didik_kota = siswa.get("peserta_didik_kota", "")
    peserta_didik_kode_pos = siswa.get("peserta_didik_kode_pos", "")
    sekolah_nama = siswa.get("sekolah_nama", "")
    sekolah_alamat = siswa.get("sekolah_alamat", "")
    sekolah_rt_rw = siswa.get("sekolah_rt_rw", "")
    sekolah_kelurahan = siswa.get("sekolah_kelurahan", "")
    sekolah_kecamatan = siswa.get("sekolah_kecamatan", "")
    sekolah_kota = siswa.get("sekolah_kota", "")
    sekolah_kode_pos = siswa.get("sekolah_kode_pos", "")
    ttd_nama_lengkap = siswa.get("ttd_nama_lengkap", "")
    ttd_tanda_tangan = siswa.get("ttd_tanda_tangan", "")
    pernyataan_nama_peserta_didik = siswa.get("pernyataan_nama_peserta_didik", "")
    pernyataan_nisn = siswa.get("pernyataan_nisn", "")
    pernyataan_kelas = siswa.get("pernyataan_kelas", "")
    pernyataan_sekolah = siswa.get("pernyataan_sekolah", "")
    pernyataan_nama_orang_tua = siswa.get("pernyataan_nama_orang_tua", "")
    pernyataan_alamat = siswa.get("pernyataan_alamat", "")
    pernyataan_ttd_orang_tua = siswa.get("pernyataan_ttd_orang_tua", "")
    pernyataan_ttd_penerima = siswa.get("pernyataan_ttd_penerima", "")

    if peserta_didik_jenis_kelamin == "laki-laki":
        FIELDS_DATA_SISWA["peserta_didik_jenis_kelamin"]["x"] = 360
    else:
        FIELDS_DATA_SISWA["peserta_didik_jenis_kelamin"]["x"] = 290

    # Kelompokkan field berdasarkan halaman
    page_data = {}

    field_map = [
        ("tanggal_surat", tanggal_surat),
        ("pemohon_nama", pemohon_nama),
        ("pemohon_alamat", pemohon_alamat),
        ("pemohon_rt_rw", pemohon_rt_rw),
        ("pemohon_kelurahan", pemohon_kelurahan),
        ("pemohon_kecamatan", pemohon_kecamatan),
        ("pemohon_kota", pemohon_kota),
        ("pemohon_kode_pos", pemohon_kode_pos),
        ("pemohon_telpon", pemohon_telpon),
        ("peserta_didik_nama", peserta_didik_nama),
        ("peserta_didik_tempat_tanggal_lahir", f"{peserta_didik_tempat_lahir}, {peserta_didik_tanggal_lahir}"),
        ("peserta_didik_jenis_kelamin", "======="),
        ("peserta_didik_alamat", peserta_didik_alamat),
        ("peserta_didik_rt_rw", peserta_didik_rt_rw),
        ("peserta_didik_kelurahan", peserta_didik_kelurahan),
        ("peserta_didik_kecamatan", peserta_didik_kecamatan),
        ("peserta_didik_kota", peserta_didik_kota),
        ("peserta_didik_kode_pos", peserta_didik_kode_pos),
        ("sekolah_nama", sekolah_nama),
        ("sekolah_alamat", sekolah_alamat),
        ("sekolah_rt_rw", sekolah_rt_rw),
        ("sekolah_kelurahan", sekolah_kelurahan),
        ("sekolah_kecamatan", sekolah_kecamatan),
        ("sekolah_kota", sekolah_kota),
        ("sekolah_kode_pos", sekolah_kode_pos),
        ("ttd_nama_lengkap", ttd_nama_lengkap),
        ("ttd_tanda_tangan", get_upload_path(ttd_tanda_tangan)),
        ("pernyataan_nama_peserta_didik", pernyataan_nama_peserta_didik),
        ("pernyataan_nisn", pernyataan_nisn),
        ("pernyataan_kelas", pernyataan_kelas),
        ("pernyataan_sekolah", pernyataan_sekolah),
        ("pernyataan_nama_orang_tua", pernyataan_nama_orang_tua),
        ("pernyataan_alamat", pernyataan_alamat),
        ("pernyataan_ttd_orang_tua", get_upload_path(pernyataan_ttd_orang_tua)),
        ("pernyataan_ttd_penerima", get_upload_path(pernyataan_ttd_penerima)),
        ("pernyataan_ttd_orang_tua_text", pernyataan_nama_orang_tua),
        ("pernyataan_ttd_penerima_text", pernyataan_nama_peserta_didik),
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

