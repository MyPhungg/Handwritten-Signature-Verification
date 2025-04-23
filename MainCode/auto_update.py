# auto_update.py
from app import app
import schedule
import threading
import time
from models import KhachHang, cap_nhat_cap_bac,initialize_signature_vectors

def run_update():
    with app.app_context():
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
