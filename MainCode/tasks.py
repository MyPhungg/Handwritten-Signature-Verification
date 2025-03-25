from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Lấy ngày đầu và cuối của tháng trước
today = datetime.now()
first_day_of_current_month = today.replace(day=1)
last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

# Chỉ lấy giao dịch trong tháng trước
tong = db.session.query(func.sum(LichSuGiaoDich.GiaTriGD)).filter(
    LichSuGiaoDich.TKGD == tai_khoan.MaTK,
    LichSuGiaoDich.ChieuGD == 1,
    LichSuGiaoDich.NgayGD >= first_day_of_previous_month,
    LichSuGiaoDich.NgayGD <= last_day_of_previous_month
).scalar() or 0