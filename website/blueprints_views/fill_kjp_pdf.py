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


# ─────────────────────────────────────────
# Koordinat field dalam PDF (satuan: points)
# Sistem koordinat PDF: y=0 di BAWAH halaman
# PDF size: w=595.44, h=841.92
# ─────────────────────────────────────────

PDF_W = 595.44
PDF_H = 841.92

def top_to_pdf_y(top, h=PDF_H):
    """Konversi koordinat 'top' (y dari atas) ke koordinat PDF (y dari bawah)."""
    return h - top


# Field definitions: (page_index, x, pdf_y, max_width, font_size) * 0.479
# page_index = 0-based (page 0 = halaman 1, page 1 = halaman 2, dst)
FIELDS = {
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
}


def _make_overlay(page_fields, page_w, page_h):
    """Buat overlay PDF transparan berisi teks untuk satu halaman."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_w, page_h))

    for field_name, value, cfg in page_fields:
        font_size = cfg.get("font_size", 10)

        # ── LANGKAH 2: Tulis teks di atas kotak putih ──
        c.setFillColor(colors.black)
        c.setFont("Helvetica", font_size)

        # Potong teks jika melebihi lebar maksimal
        text = str(value)
        while text and c.stringWidth(text, "Helvetica", font_size) > cfg["max_w"]:
            text = text[:-1]

        c.drawString(cfg["x"], cfg["y"], text)

    c.save()
    packet.seek(0)
    return PdfReader(packet)


def fill_kjp_pdf(siswa: dict, template_path: str = "formulir_kjp.pdf") -> bytes:
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

    # Cek Jenis Kelamin
    if jenis_kelamin_murid == "Laki-laki":
        FIELDS["jenis_kelamin_murid"]["x"] = 234
        FIELDS["jenis_kelamin_murid"]["y"] = top_to_pdf_y(200)
    else:
        FIELDS["jenis_kelamin_murid"]["x"] = 313
        FIELDS["jenis_kelamin_murid"]["y"] = top_to_pdf_y(200)

    # Cek kelas
    if kelas == "7":
        FIELDS["kelas"]["x"] = 388
        FIELDS["kelas"]["y"] = top_to_pdf_y(371)
    elif kelas == "8":
        FIELDS["kelas"]["x"] = 388
        FIELDS["kelas"]["y"] = top_to_pdf_y(384)
    elif kelas == "9":
        FIELDS["kelas"]["x"] = 388
        FIELDS["kelas"]["y"] = top_to_pdf_y(396)
    else:
        FIELDS["kelas"]["x"] = 0
        FIELDS["kelas"]["y"] = top_to_pdf_y(0)

    # Cek Masa Berlaku Identitas
    if masa_berlaku_identitas == "Seumur Hidup":
        FIELDS["masa_berlaku_identitas"]["x"] = 307
        FIELDS["masa_berlaku_identitas"]["y"] = top_to_pdf_y(440)
    else:
        FIELDS["masa_berlaku_identitas"]["x"] = 222
        FIELDS["masa_berlaku_identitas"]["y"] = top_to_pdf_y(437)

    # Cek Alamat Surat
    if alamat_surat == "Diambil Sendiri":
        FIELDS["alamat_surat"]["x"] = 236
        FIELDS["alamat_surat"]["y"] = top_to_pdf_y(487)
    elif alamat_surat == "Dikirim":
        FIELDS["alamat_surat"]["x"] = 344
        FIELDS["alamat_surat"]["y"] = top_to_pdf_y(487)

    # Cek Tipe Alamat
    if tipe_alamat == "Alamat Rumah":
        FIELDS["tipe_alamat"]["x"] = 236
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(508)
    elif tipe_alamat == "Alamat Kantor":
        FIELDS["tipe_alamat"]["x"] = 236
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(520)
    elif tipe_alamat == "Alamat Kost":
        FIELDS["tipe_alamat"]["x"] = 236
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(533)
    elif tipe_alamat == "Alamat Sesuai KK":
        FIELDS["tipe_alamat"]["x"] = 236
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(546)
    elif tipe_alamat == "Alamat Sesuai NPWP":
        FIELDS["tipe_alamat"]["x"] = 344
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(508)
    elif tipe_alamat == "Alamat Rusun":
        FIELDS["tipe_alamat"]["x"] = 344
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(519)
    elif tipe_alamat == "Alamat Panti":
        FIELDS["tipe_alamat"]["x"] = 344
        FIELDS["tipe_alamat"]["y"] = top_to_pdf_y(534)

    # Cek Status Tempat Tinggal
    if status_tempat_tinggal == "Bukan Milik Pribadi":
        FIELDS["status_tempat_tinggal"]["x"] = 237
        FIELDS["status_tempat_tinggal"]["y"] = top_to_pdf_y(560)
    elif status_tempat_tinggal == "Milik Pribadi":
        FIELDS["status_tempat_tinggal"]["x"] = 392
        FIELDS["status_tempat_tinggal"]["y"] = top_to_pdf_y(560)

    # Cek Agama Murid
    if agama_murid == "Islam":
        FIELDS["agama_murid"]["x"] = 310
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(596)
    if agama_murid == "Protestan":
        FIELDS["agama_murid"]["x"] = 310
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Katolik":
        FIELDS["agama_murid"]["x"] = 391
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Hindu":
        FIELDS["agama_murid"]["x"] = 237
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(582)
    if agama_murid == "Budha":
        FIELDS["agama_murid"]["x"] = 237
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(596)
    if agama_murid == "Lainnya":
        FIELDS["agama_murid"]["x"] = 391
        FIELDS["agama_murid"]["y"] = top_to_pdf_y(596)

    # Cek untuk Disabilitas
    if untuk_disabilitas == "Tidak Ada":
        FIELDS["untuk_disabilitas"]["x"] = 0
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(0)
    elif untuk_disabilitas == "Tuna Rungu":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(664)
    elif untuk_disabilitas == "Tuna Netra":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(676)
    elif untuk_disabilitas == "Tuna Wicara":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(690)
    elif untuk_disabilitas == "Tuna Daksa":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(703)
    elif untuk_disabilitas == "Tuna Grahita":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(716)
    elif untuk_disabilitas == "Tuna Laras":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(729)
    elif untuk_disabilitas == "Tuna Ganda":
        FIELDS["untuk_disabilitas"]["x"] = 237
        FIELDS["untuk_disabilitas"]["y"] = top_to_pdf_y(743)

    # Kelompokkan field berdasarkan halaman
    page_data = {}

    field_map = [
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
    ]

    for field_key, value in field_map:
        cfg = FIELDS[field_key]
        pg  = cfg["page"]
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
            overlay_page   = overlay_reader.pages[0]
            page.merge_page(overlay_page)

        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()


# # ─────────────────────────────────────────
# # Contoh penggunaan standalone (bukan Flask)
# # ─────────────────────────────────────────
# if __name__ == "__main__":
#     import os

#     # Simulasi data dari database
#     sample_data = [
#         {"id": 1, "tanggal": "2026-01-10", "nama": "Budi Santoso",      "no_telepon": "081234567890", "keterangan": "Siswa kelas 8A"},
#         {"id": 2, "tanggal": "2026-01-11", "nama": "Siti Rahayu",        "no_telepon": "089876543210", "keterangan": "Siswa kelas 7B"},
#         {"id": 3, "tanggal": "2026-01-12", "nama": "Ahmad Fauzi Pratama","no_telepon": "082111222333", "keterangan": "Siswa kelas 9C"},
#     ]

#     os.makedirs("output_pdf", exist_ok=True)

#     for siswa in sample_data:
#         pdf_bytes = fill_kjp_pdf(siswa, template_path="formulir_kjp.pdf")
#         nama_file = siswa["nama"].replace(" ", "_")
#         out_path  = f"output_pdf/KJP_{nama_file}.pdf"
#         with open(out_path, "wb") as f:
#             f.write(pdf_bytes)
#         print(f"✓ Dibuat: {out_path}")

#     print("\nSelesai! Cek folder output_pdf/")

# import io
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors

# PDF_W = 595.44
# PDF_H = 841.92

# def top_to_pdf_y(top, h=PDF_H):
#     return h - top

# FIELDS = {
#     "nama_cover": {
#         "page": 0,
#         "x": 280.0,
#         "y": top_to_pdf_y(524.4),
#         "max_w": 145,
#         "font_size": 10,
#         "cover_dots": (264.6, 512.4, 423.2, 524.4),
#     },

#     "nama_h2": {
#         "page": 1,
#         "x": 221.4,
#         "y": top_to_pdf_y(188.1),
#         "max_w": 170,
#         "font_size": 9,
#         "cover_dots": (221.4, 177.0, 394.1, 188.1),
#     },
#     "no_hp": {
#         "page": 1,
#         "x": 221.4,
#         "y": top_to_pdf_y(459.6),
#         "max_w": 170,
#         "font_size": 9,
#         "cover_dots": (221.4, 448.6, 394.1, 459.6),
#     },
#     "no_telepon": {
#         "page": 1,
#         "x": 221.4,
#         "y": top_to_pdf_y(475.0),
#         "max_w": 170,
#         "font_size": 9,
#         "cover_dots": (221.4, 463.9, 394.1, 475.0),
#     },

#     "nama_surat": {
#         "page": 4,
#         "x": 140.0,
#         "y": top_to_pdf_y(340.0),
#         "max_w": 350,
#         "font_size": 10,
#         "cover_dots": (140.0, 329.0, 490.0, 340.0),
#     },
# }


# def _make_overlay(page_fields, page_w, page_h):
#     packet = io.BytesIO()
#     c = canvas.Canvas(packet, pagesize=(page_w, page_h))

#     for field_name, value, cfg in page_fields:
#         font_size = cfg.get("font_size", 10)

#         if "cover_dots" in cfg:
#             x1, top, x2, bottom = cfg["cover_dots"]
#             rect_y      = page_h - bottom
#             rect_height = bottom - top
#             rect_width  = x2 - x1

#             c.setFillColor(colors.white)
#             c.setStrokeColor(colors.white)
#             c.rect(x1, rect_y, rect_width, rect_height, fill=1, stroke=0)

#         c.setFillColor(colors.black)
#         c.setFont("Helvetica", font_size)

#         text = str(value)
#         while text and c.stringWidth(text, "Helvetica", font_size) > cfg["max_w"]:
#             text = text[:-1]

#         c.drawString(cfg["x"], cfg["y"], text)

#     c.save()
#     packet.seek(0)
#     return PdfReader(packet)


# def fill_kjp_pdf(siswa: dict, template_path: str = "formulir_kjp.pdf") -> bytes:
#     nama        = siswa.get("nama", "")
#     no_telepon  = siswa.get("no_telepon", "")
#     keterangan  = siswa.get("keterangan", "")
#     tanggal     = siswa.get("tanggal", "")

#     page_data = {}

#     field_map = [
#         ("nama_cover",  nama),
#         ("nama_h2",     nama),
#         ("no_hp",       no_telepon),
#         ("no_telepon",  no_telepon),
#         ("nama_surat",  nama),
#     ]

#     for field_key, value in field_map:
#         cfg = FIELDS[field_key]
#         pg  = cfg["page"]
#         if pg not in page_data:
#             page_data[pg] = []
#         page_data[pg].append((field_key, value, cfg))

#     # Baca template
#     reader = PdfReader(template_path)
#     writer = PdfWriter()

#     for i, page in enumerate(reader.pages):
#         page_w = float(page.mediabox.width)
#         page_h = float(page.mediabox.height)

#         if i in page_data:
#             overlay_reader = _make_overlay(page_data[i], page_w, page_h)
#             overlay_page   = overlay_reader.pages[0]
#             page.merge_page(overlay_page)

#         writer.add_page(page)

#     output = io.BytesIO()
#     writer.write(output)
#     output.seek(0)
#     return output.read()
