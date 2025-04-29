# auto_update.py
from flask import current_app

import schedule
import threading
import time
from models import KhachHang, cap_nhat_cap_bac, initialize_signature_vectors
import mysql.connector
import numpy as np

def run_update():
    with current_app.app_context():
        print("Đang cập nhật dữ liệu...")
        all_kh = KhachHang.query.all()
        initialize_signature_vectors()
        for kh in all_kh:
            cap_nhat_cap_bac(kh.MaKH)
        print("Xong!")

schedule.every(1).hours.do(run_update)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_update_thread():
    thread = threading.Thread(target=run_schedule)
    thread.daemon = True
    thread.start()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bank"
    )

def get_transaction_data(as_list=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(NgayGD, '%Y-%m') AS month,
               SUM(CASE WHEN ChieuGD=1 THEN GiaTriGD ELSE 0 END),
               SUM(CASE WHEN ChieuGD=0 THEN GiaTriGD ELSE 0 END)
        FROM lichsugiaodich
        GROUP BY month
    """)
    results = cursor.fetchall()

    months = [row[0] for row in results]
    money_in = [float(row[1]) for row in results]
    money_out = [float(row[2]) for row in results]

    if as_list:
        cursor.execute("SELECT magd, NgayGD, ChieuGD, GiaTriGD FROM lichsugiaodich")
        all_tx = cursor.fetchall()
        transactions = [{"id": r[0], "NgayGD": r[1].strftime("%Y-%m-%d"), "ChieuGD": r[2], "GiaTriGD": float(r[3])} for r in all_tx]
        cursor.close()
        conn.close()
        return transactions

    cursor.close()
    conn.close()
    return {
        "months": months,
        "money_in": money_in,
        "money_out": money_out
    }

def get_savings_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NgayMo, SoTienGui, LaiSuat FROM savingssotietkiem")
    rows = cursor.fetchall()

    years = []
    savings_growth = []

    for row in rows:
        start_year = row[0].year
        sotien = row[1]
        laisuat = row[2]
        years.append(start_year)
        growth = sotien * (1 + laisuat)
        savings_growth.append(growth)

    cursor.close()
    conn.close()

    return {
        "years": years,
        "savings_growth": savings_growth
    }

def get_danhmuc_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MaDM, TenDM FROM danhmucchitieu")
    rows = cursor.fetchall()
    data = [{"MaDM": r[0], "TenDM": r[1]} for r in rows]
    cursor.close()
    conn.close()
    return data

def get_expense_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dm.TenDM, SUM(gd.GiaTriGD)
        FROM lichsugiaodich gd
        JOIN danhmucchitieu dm ON gd.MaDM = dm.MaDM
        WHERE gd.ChieuGD = 0
        GROUP BY dm.TenDM
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"category": row[0], "total": float(row[1])} for row in rows]
