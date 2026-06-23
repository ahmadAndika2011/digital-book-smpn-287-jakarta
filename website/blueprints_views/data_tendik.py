from flask import Blueprint, render_template, redirect, url_for, request
from ..models import DatabaseTendik
from .. import db

views = Blueprint("data_tendik", __name__)

def get_data_guru(q=None):
    list_data_guru = DatabaseTendik.query
    if q:
        list_data_guru = list_data_guru.filter(
            db.or_(
                DatabaseTendik.name.ilike(f"%{q}%"),
                DatabaseTendik.mapel.ilike(f"%{q}%"),
                DatabaseTendik.status.ilike(f"%{q}%"),
            )
        ).all()
    else:
        list_data_guru = list_data_guru.order_by(DatabaseTendik.name.asc()).all()
        
    for guru in list_data_guru:
        yield guru

@views.route("/data-tendik")
def data_tendik():
    q = request.args.get("q")
    list_data_guru = get_data_guru(q)
    jumlah_status_pns = DatabaseTendik.query.filter_by(status="PNS").count()
    jumlah_status_p3k = DatabaseTendik.query.filter_by(status="PPPK").count()
    jumlah_status_kki = DatabaseTendik.query.filter_by(status="KKI").count()
    return render_template("data-tendik.html", 
                           list_data_guru=list_data_guru, 
                           jumlah_status_pns=jumlah_status_pns, 
                           jumlah_status_kki=jumlah_status_kki, 
                           jumlah_status_p3k=jumlah_status_p3k,
                           data="Tendik",
                           detail="detail_tendik")