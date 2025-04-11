import schedule
import time
from flask import Flask
from models import db, KhachHang, cap_nhat_cap_bac

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank'
db.init_app(app)

def run_update():
    with app.app_context():
        print("Chạy cập nhật tự động...")
        all_kh = KhachHang.query.all()
        for kh in all_kh:
            cap_nhat_cap_bac(kh.MaKH)
        print("Cập nhật hoàn tất!")

# Chạy mỗi 1 giờ
schedule.every(1).hours.do(run_update)

while True:
    schedule.run_pending()
    time.sleep(60)
