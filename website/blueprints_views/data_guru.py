from flask import Blueprint, render_template, redirect, url_for, request
from ..models import DatabaseGuru
from .. import db

views = Blueprint("data_guru", __name__)

def get_data_guru(q=None):
    list_data_guru = DatabaseGuru.query
    if q:
        list_data_guru = list_data_guru.filter(
            db.or_(
                DatabaseGuru.name.ilike(f"%{q}%"),
                DatabaseGuru.mapel.ilike(f"%{q}%"),
                DatabaseGuru.status.ilike(f"%{q}%"),
            )
        ).all()
    else:
        list_data_guru = list_data_guru.order_by(DatabaseGuru.name.asc()).all()
        
    for guru in list_data_guru:
        yield guru

@views.route("/data-guru")
def data_guru():
    q = request.args.get("q")
    # if q:
    #     list_data_guru = DatabaseGuru.query.filter(
    #         db.or_(
    #             DatabaseGuru.name.ilike(f"%{q}%"),
    #             DatabaseGuru.mapel.ilike(f"%{q}%"),
    #             DatabaseGuru.status.ilike(f"%{q}%"),
    #         )
    #     ).all()
    # else:
    #     list_data_guru = DatabaseGuru.query.order_by(DatabaseGuru.name.asc()).all()
    list_data_guru = get_data_guru(q)
    jumlah_status_pns = DatabaseGuru.query.filter_by(status="PNS").count()
    jumlah_status_p3k = DatabaseGuru.query.filter_by(status="PPPK").count()
    jumlah_status_kki = DatabaseGuru.query.filter_by(status="KKI").count()
    return render_template("data-guru.html", 
                           list_data_guru=list_data_guru, 
                           jumlah_status_pns=jumlah_status_pns, 
                           jumlah_status_kki=jumlah_status_kki, 
                           jumlah_status_p3k=jumlah_status_p3k)