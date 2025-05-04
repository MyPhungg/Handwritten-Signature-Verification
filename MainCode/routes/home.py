from sqlalchemy import func, cast, Integer
from werkzeug.utils import secure_filename
import os
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
import io
import matplotlib.pyplot as plt
from sqlalchemy.sql import func
from sqlalchemy import event
from sqlalchemy import or_
from models import db, TaiKhoan, KhachHang, CapBacKH, LoaiTK, KhuyenMai, LichSuGiaoDich, LichSuTichDiem, NhanVien, SavingsSoTietKiem
import string
import random
import re
from decimal import Decimal
from datetime import datetime, date
from models import db, TaiKhoan, KhachHang, CapBacKH, LoaiTK, KhuyenMai, LichSuGiaoDich, AccountKH
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')


home_bp = Blueprint('home', __name__)


# Kiểm tra xem đã chọn tại khoản chưa
@home_bp.route('/home')
def home():
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/home.html', isLogin=isLogin, tk=tk)


# Hiển thị thông tin người dùng
@home_bp.route('/infoUser')
def infoUser():
    if 'MaKH' not in session:
        flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
        return redirect(url_for('auth.login'))
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))
    maKH = session['MaKH']
    maTK = session['MaTK']
    info = KhachHang.query.filter_by(MaKH=maKH).first()
    infoCard = (TaiKhoan.query
                .join(LoaiTK, TaiKhoan.LoaiTK == LoaiTK.MaLoai)
                .join(KhachHang, TaiKhoan.MaKH == KhachHang.MaKH)
                .join(CapBacKH, KhachHang.MaCapBac == CapBacKH.MaCapBac)
                .filter(TaiKhoan.MaTK == maTK, KhachHang.MaKH == maKH)
                .first()
                )
    if not info or not infoCard:
        flash('Không tìm thấy thông tin khách hàng hoặc thẻ!', 'error')
        return redirect(url_for('home.home'))
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/infoUser.html', info=info, infoCard=infoCard, isLogin=isLogin, tk=tk)


# Tải thông tin vào trang đổi thông tin
@home_bp.route('/infoUser/inputForm')
def inputForm():
    if 'MaKH' not in session:
        flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
        return redirect(url_for('auth.login'))
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))
    maKH = session['MaKH']
    info = KhachHang.query.filter_by(MaKH=maKH).first()
    if not info:
        flash('Không tìm thấy thông tin khách hàng!', 'error')
        return redirect(url_for('home.home'))
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/changeInfoUser.html', info=info, isLogin=isLogin, tk=tk)

# Đổi thông tin người dùng


@home_bp.route('/infoUser/inputForm/changeInfoUser', methods=['GET', 'POST'])
def changeInfoUser():
    if 'MaKH' not in session:
        flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
        return redirect(url_for('auth.login'))
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))
    if request.method == 'POST':
        errors = validate_input(request.form)
        if errors:
            for field, message in errors.items():
                flash(message, 'error')
            return redirect(url_for('home.inputForm'))

        # Nếu tất cả validate thành công
        maKH = session['MaKH']
        khachhang = KhachHang.query.filter_by(MaKH=maKH).first()

        if khachhang:
            # Cập nhật thông tin từ request form
            khachhang.HoTen = request.form.get('hoten', khachhang.HoTen)
            khachhang.SoCCCD = request.form.get('cccd', khachhang.SoCCCD)
            khachhang.NoiCapCCCD = request.form.get(
                'noicapcccd', khachhang.NoiCapCCCD)
            khachhang.QuocTich = request.form.get(
                'quoctich', khachhang.QuocTich)
            khachhang.NoiCuTru = request.form.get(
                'noicutru', khachhang.NoiCuTru)
            khachhang.DiaChiThuongTru = request.form.get(
                'diachithuongtru', khachhang.DiaChiThuongTru)
            khachhang.SoDienThoai = request.form.get(
                'sodienthoai', khachhang.SoDienThoai)
            khachhang.Email = request.form.get('email', khachhang.Email)
            khachhang.NgaySinh = request.form.get(
                'ngaysinh', khachhang.NgaySinh)
            khachhang.NgayCapCCCD = request.form.get(
                'ngaycapcccd', khachhang.NgayCapCCCD)
            khachhang.CoGiaTriDen = request.form.get(
                'cogiatriden', khachhang.CoGiaTriDen)
            khachhang.DanToc = request.form.get('dantoc', khachhang.DanToc)
            khachhang.DiaChiHienTai = request.form.get(
                'diachihientai', khachhang.DiaChiHienTai)
            khachhang.GioiTinh = request.form.get(
                'gioitinh', khachhang.GioiTinh)
            khachhang.NgheNghiep = request.form.get(
                'nghenghiep', khachhang.NgheNghiep)

            # Lưu thay đổi
            db.session.commit()
            flash('Thông tin của bạn đã được cập nhật!', 'success')
            return redirect(url_for('home.infoUser'))
        else:
            flash('Cập nhật thông tin thất bại! Không tìm thấy người dùng!', 'error')

    return redirect(url_for('home.inputForm'))

# Regex


# Định nghĩa regex
patterns = {
    "hoten": (re.compile(r"^[a-zA-ZÀ-ỹ\s]+$"), "Họ tên chỉ chứa chữ cái và dấu cách"),
    "cccd": (re.compile(r"^\d{12}$"), "CCCD phải có đúng 12 chữ số"),
    "noicapcccd": (re.compile(r"^[\w\sÀ-ỹ]+$", re.UNICODE), "Nơi cấp CCCD chỉ chứa chữ cái và dấu cách"),
    "quoctich": (re.compile(r"^[\w\sÀ-ỹ]+$", re.UNICODE), "Quốc tịch chỉ chứa chữ cái và dấu cách"),
    "noicutru": (re.compile(r"^[\w\d\s,.-À-ỹ]+$", re.UNICODE), "Nơi cư trú không hợp lệ"),
    "diachithuongtru": (re.compile(r"^[\w\d\s,.-À-ỹ]+$", re.UNICODE), "Địa chỉ thường trú không hợp lệ"),
    "sodienthoai": (re.compile(r"^0\d{9}$"), "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0"),
    "email": (re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"), "Email không hợp lệ"),
    "ngaysinh": (re.compile(r"^\d{4}-\d{2}-\d{2}$"), "Ngày sinh phải có định dạng YYYY-MM-DD"),
    "ngaycapcccd": (re.compile(r"^\d{4}-\d{2}-\d{2}$"), "Ngày cấp CCCD phải có định dạng YYYY-MM-DD"),
    "cogiatriden": (re.compile(r"^\d{4}-\d{2}-\d{2}$"), "Có giá trị đến phải có định dạng YYYY-MM-DD"),
    "dantoc": (re.compile(r"^[\w\sÀ-ỹ]+$", re.UNICODE), "Dân tộc chỉ chứa chữ cái và dấu cách"),
    "diachihientai": (re.compile(r"^[\w\d\s,.-À-ỹ]+$", re.UNICODE), "Địa chỉ hiện tại không hợp lệ"),
    "gioitinh": (re.compile(r"^(Nam|Nữ|Khác)$"), "Giới tính chỉ có thể là Nam, Nữ hoặc Khác"),
    "nghenghiep": (re.compile(r"^[\w\sÀ-ỹ]+$", re.UNICODE), "Nghề nghiệp chỉ chứa chữ cái và dấu cách"),
}

# Nạp tiền


@home_bp.route('/napTien', methods=['POST', 'GET'])
def napTien():
    if request.method == 'POST':
        # Lấy MaGD
        last = LichSuGiaoDich.query.order_by(
            cast(func.substr(LichSuGiaoDich.MaGD, 3), Integer).desc()
        ).first()
        if last and last.MaGD[2:].isdigit():
            maGD = f"GD{int(last.MaGD[2:]) + 1}"
        else:
            maGD = "GD1"

        noiDung = request.form['noiDung']
        soTien = request.form['soTien']
        chieuGD = 1
        ngayGD = (datetime.now()).strftime("%Y-%m-%d %H-%M-%S")
        TKGD = session['MaTK']
        hinhThuc = "Nạp tiền"
        giao_dich_moi = LichSuGiaoDich(
            MaGD=maGD,
            NgayGD=ngayGD,
            ChieuGD=chieuGD,
            NoiDungGD=noiDung,
            GiaTriGD=soTien,
            HinhThuc=hinhThuc,
            TKGD=TKGD
        )
        taikhoan = TaiKhoan.query.get(TKGD)
        taikhoan.SoDu += int(soTien)
        db.session.add(giao_dich_moi)
        cap_nhat_diem_va_cap_bac(TKGD, int(soTien))
        db.session.commit()
        flash('Nạp tiền thành công!', 'success')
        return redirect(url_for('home.napTien'))
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/NapTien.html', isLogin=isLogin, tk=tk)


def validate_input(data):
    errors = {}

    for field, (pattern, error_msg) in patterns.items():
        value = data.get(field, "").strip()
        if not pattern.match(value):
            errors[field] = error_msg  # Lưu thông báo lỗi nếu không khớp regex

    return errors  # Trả về dict lỗi, rỗng nếu không có lỗi


# -------------Quản lý tài khoản-------------------
@home_bp.route('/admin/taikhoan')
def admin_taikhoan():
    tai_khoan_list = TaiKhoan.query.all()  # Lấy tất cả khách hàng từ database
    return render_template('admin/chinhsuaTK.html', tai_khoan_list=tai_khoan_list)

# TÌM KIẾM TÀI KHOẢN


@home_bp.route('/taikhoan/timkiem', methods=['GET'])
def tim_kiem_taikhoan():
    search_query = request.args.get('search', '').strip()

    if search_query:
        tai_khoan_list = TaiKhoan.query.join(KhachHang).filter(
            KhachHang.HoTen.ilike(f"%{search_query}%")
        ).all()
    else:
        tai_khoan_list = TaiKhoan.query.all()

    return render_template('admin/chinhsuaTK.html', tai_khoan_list=tai_khoan_list, search_query=search_query)

# TỰ ĐỘNG ĐÓNG TÀI KHOẢN NẾU QUÁ 1 THÁNG CHƯA MỞ LẠI


def dong_tai_khoan(maTK):
    tai_khoan = TaiKhoan.query.get(maTK)
    if tai_khoan:
        tai_khoan.TrangThai = 0  # Đánh dấu tài khoản là đã đóng
        tai_khoan.ThoiGianDong = datetime.now()  # Lưu thời gian đóng
        db.session.commit()


def xoa_tai_khoan_cu():
    # Lấy tất cả các tài khoản bị đóng
    tai_khoan_dong = TaiKhoan.query.filter(TaiKhoan.TrangThai == 0).all()

    for tai_khoan in tai_khoan_dong:
        if tai_khoan.ThoiGianDong and tai_khoan.ThoiGianDong < datetime.now() - timedelta(days=30):
            # Nếu tài khoản bị đóng hơn 1 tháng, xóa nó
            db.session.delete(tai_khoan)

    db.session.commit()


def xoa_tai_khoan_cu_job():
    # Hàm gọi để xóa tài khoản cũ
    xoa_tai_khoan_cu()


# Khởi tạo scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(xoa_tai_khoan_cu_job, 'interval', days=1)  # Chạy mỗi ngày
scheduler.start()

# --------------------------------------------------#


# ------------Quản lý khách Hàng-----------------


@home_bp.route('/admin/khachhang')
def admin_khachhang():
    khach_hang_list = KhachHang.query.all()  # Lấy tất cả khách hàng từ database
    return render_template('admin/chinhsuaKH.html', khach_hang_list=khach_hang_list)


@home_bp.route('/khachhang/timkiem', methods=['GET'])
def tim_kiem_khachhang():
    search_query = request.args.get('search', '').strip()

    if search_query:
        khach_hang_list = KhachHang.query.filter(
            KhachHang.HoTen.ilike(f"%{search_query}%")).all()
    else:
        khach_hang_list = KhachHang.query.all()

    # Lấy danh sách tài khoản tương ứng với các khách hàng tìm được
    ma_kh_list = [kh.MaKH for kh in khach_hang_list]
    tai_khoan_list = TaiKhoan.query.filter(TaiKhoan.MaKH.in_(ma_kh_list)).all()

    return render_template(
        'admin/chinhsuaKH.html',
        khach_hang_list=khach_hang_list,
        tai_khoan_list=tai_khoan_list,
        search_query=search_query
    )


@home_bp.route('/admin/xoa_khachhang', methods=['POST'])
def xoa_khachhang():
    # Lấy danh sách mã khách hàng từ form
    khach_hang_ids = request.form.getlist("xoa_khachhang")

    if not khach_hang_ids:
        flash("Vui lòng chọn ít nhất một khách hàng để xóa.", "warning")
        return redirect(url_for('home.admin_khachhang'))

    try:
        for maKH in khach_hang_ids:
            khach_hang = KhachHang.query.filter_by(MaKH=maKH).first()
            if khach_hang:
                db.session.delete(khach_hang)

        db.session.commit()
        flash("Xóa khách hàng thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Lỗi khi xóa khách hàng: " + str(e), "danger")

    return redirect(url_for('home.admin_khachhang'))


@home_bp.route('/khachhang/<maKH>')
def chi_tiet_khachhang(maKH):
    khach_hang = KhachHang.query.get(maKH)
    if not khach_hang:
        flash('Không tìm thấy khách hàng!', 'error')
        return redirect(url_for('home.admin_khachhang'))
    return render_template('admin/chitietKH.html', khach_hang=khach_hang)


def generate_ma_kh():
    # Lấy khách hàng có mã lớn nhất theo số sau "KH"
    last_kh = KhachHang.query.order_by(
        db.cast(db.func.substr(KhachHang.MaKH, 3), db.Integer).desc()
    ).first()

    if last_kh:
        # Trích số nguyên sau "KH"
        last_id = int(last_kh.MaKH[2:])
        new_id = f"KH{last_id + 1}"
    else:
        new_id = "KH1"

    return new_id


@home_bp.route("/them_khachhang", methods=["GET", "POST"])
def them_khachhang():
    if request.method == "POST":
        try:
            ma_kh = generate_ma_kh()  # Tự động sinh MaKH
            ho_ten = request.form.get("HoTen")
            ngay_sinh = datetime.strptime(
                request.form.get("NgaySinh"), "%Y-%m-%d")
            so_cccd = request.form.get("SoCCCD")
            ngay_cap_cccd = datetime.strptime(
                request.form.get("NgayCapCCCD"), "%Y-%m-%d")
            noi_cap_cccd = request.form.get("NoiCapCCCD")
            co_gia_tri_den = datetime.strptime(
                request.form.get("CoGiaTriDen"), "%Y-%m-%d")
            quoc_tich = request.form.get("QuocTich")
            dan_toc = request.form.get("DanToc")
            noi_cu_tru = request.form.get("NoiCuTru")
            dia_chi_hien_tai = request.form.get("DiaChiHienTai")
            dia_chi_thuong_tru = request.form.get("DiaChiThuongTru")
            gioi_tinh = request.form.get("GioiTinh")
            so_dien_thoai = request.form.get("SoDienThoai")
            nghe_nghiep = request.form.get("NgheNghiep")
            email = request.form.get("Email")

            ma_nvql = "NV1"  # Mặc định là NV1
            ma_cap_bac = "CB1"  # Mặc định là CB1
            chu_ky = request.form.get("ChuKy") or "DEFAULT_CHUKY"

            khach_hang = KhachHang(
                MaKH=ma_kh,
                HoTen=ho_ten,
                NgaySinh=ngay_sinh,
                SoCCCD=so_cccd,
                NgayCapCCCD=ngay_cap_cccd,
                NoiCapCCCD=noi_cap_cccd,
                CoGiaTriDen=co_gia_tri_den,
                QuocTich=quoc_tich,
                DanToc=dan_toc,
                NoiCuTru=noi_cu_tru,
                DiaChiHienTai=dia_chi_hien_tai,
                DiaChiThuongTru=dia_chi_thuong_tru,
                GioiTinh=gioi_tinh,
                SoDienThoai=so_dien_thoai,
                NgheNghiep=nghe_nghiep,
                Email=email,
                MaNVQL=ma_nvql,
                MaCapBac=ma_cap_bac,
                ChuKy=chu_ky
            )

            db.session.add(khach_hang)
            db.session.commit()

            flash("Thêm khách hàng thành công!", "success")
            return redirect(url_for("home.them_khachhang", maKH=ma_kh))

        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi thêm khách hàng: {str(e)}", "danger")

    return render_template("admin/themKH.html")


@home_bp.route('/khachhang/sua/<maKH>', methods=['GET', 'POST'])
def sua_khachhang(maKH):
    khach_hang = KhachHang.query.get(maKH)
    if not khach_hang:
        flash('Không tìm thấy khách hàng!', 'error')
        return redirect(url_for('home.admin_khachhang'))

    danh_sach_nhan_vien = NhanVien.query.all()
    danh_sach_cap_bac = CapBacKH.query.all()

    if request.method == 'POST':
        try:
            khach_hang.HoTen = request.form.get("HoTen")
            khach_hang.NgaySinh = datetime.strptime(
                request.form.get("NgaySinh"), "%Y-%m-%d")
            khach_hang.SoCCCD = request.form.get("SoCCCD")
            khach_hang.NgayCapCCCD = datetime.strptime(
                request.form.get("NgayCapCCCD"), "%Y-%m-%d")
            khach_hang.NoiCapCCCD = request.form.get("NoiCapCCCD")
            khach_hang.CoGiaTriDen = datetime.strptime(
                request.form.get("CoGiaTriDen"), "%Y-%m-%d")
            khach_hang.QuocTich = request.form.get("QuocTich")
            khach_hang.DanToc = request.form.get("DanToc")
            khach_hang.NoiCuTru = request.form.get("NoiCuTru")
            khach_hang.DiaChiHienTai = request.form.get("DiaChiHienTai")
            khach_hang.DiaChiThuongTru = request.form.get("DiaChiThuongTru")
            khach_hang.GioiTinh = request.form.get("GioiTinh")
            khach_hang.SoDienThoai = request.form.get("SoDienThoai")
            khach_hang.NgheNghiep = request.form.get("NgheNghiep")
            khach_hang.Email = request.form.get("Email")
            khach_hang.ChuKy = request.form.get("ChuKy")

            db.session.commit()
            flash("Cập nhật khách hàng thành công!", "success")
            return redirect(url_for('home.sua_khachhang', maKH=maKH))

        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi cập nhật: {str(e)}", "danger")

    return render_template('admin/chitietKH.html', khach_hang=khach_hang)


# ----------------------------------------
# --------------Giao diện khách hàng-----------
# uu dai
@home_bp.route('/uudai')
def xem_uu_dai():
    if 'MaKH' not in session or 'MaTK' not in session:
        flash('Vui lòng đăng nhập để xem ưu đãi!', 'error')
        return redirect(url_for('auth.login'))

    ma_kh = session['MaKH']

    user = KhachHang.query.get(ma_kh)

    isLogin = 'MaKH' in session
    ma_tk = session['MaTK'] if isLogin else None
    # Lấy loại tài khoản từ mã tài khoản đã chọn
    tai_khoan = TaiKhoan.query.get(ma_tk)

    loai_tk = tai_khoan.LoaiTK  # Lấy mã loại tài khoản

    # Lọc khuyến mãi theo loại tài khoản, cấp bậc và thời gian
    today = date.today()  # Chỉ cần lấy date, không cần đến datetime.today().date()
    uu_dai_list = KhuyenMai.query.filter(
        or_(KhuyenMai.LoaiTKApDung.is_(None),
            KhuyenMai.LoaiTKApDung == loai_tk),
        or_(KhuyenMai.CapBacThanhVien.is_(None),
            KhuyenMai.CapBacThanhVien == user.MaCapBac),
        func.date(KhuyenMai.ThoiGian) >= today
    ).all()

    return render_template('user/offers.html', uu_dai_list=uu_dai_list, tk=tai_khoan, current_date=today, isLogin=isLogin)


@home_bp.route('/uudai/<maKM>')
def chi_tiet_uudai(maKM):
    uu_dai = KhuyenMai.query.get(maKM)
    if not uu_dai:
        flash('Không tìm thấy ưu đãi!', 'error')
        return redirect(url_for('home.danh_sach_uudai'))
    return render_template('admin/chitietUuDai.html', uu_dai=uu_dai)


@home_bp.route('/uudai/timkiem', methods=['GET'])
def tim_kiem_uudai():
    # <<<<<<< HEAD
    #     keyword = request.args.get('keyword', '')
    #     uu_dai_list = KhuyenMai.query.filter(
    #         KhuyenMai.NoiDung.contains(keyword)).all()
    #     return render_template('user/offers.html', uu_dai_list=uu_dai_list, keyword=keyword)
    # =======
    search_query = request.args.get(
        'search', '').strip()  # Lấy từ khóa tìm kiếm

    if search_query:
        uu_dai_list = KhuyenMai.query.filter(
            KhuyenMai.NoiDung.ilike(f"%{search_query}%")).all()
    else:
        uu_dai_list = KhuyenMai.query.all()

    return render_template('admin/chinhsuaUuDai.html', uu_dai_list=uu_dai_list, search_query=search_query)

# --------------------------------

# -------------------Quản lý ưu đãi -----------------


def loadTenNhanVien():
    maNV = session['MaNV']
    info = NhanVien.query.filter_by(MaNV=maNV).first()
    if not info:
        flash('Không tìm thấy thông tin nhân viên! Vui lòng đăng nhập lại', 'error')
        return redirect(url_for('auth.login'))
    return info.HoTen


@home_bp.route('/admin/uudai')
def admin_uudai():
    ten = loadTenNhanVien()
    uu_dai_list = KhuyenMai.query.all()  # Lấy tất cả ưu đãi từ CSDL
    return render_template('admin/chinhsuaUuDai.html', uu_dai_list=uu_dai_list, ten=ten)


@home_bp.route("/them_uudai", methods=["GET", "POST"])
def them_uudai():
    danh_sach_cap_bac = CapBacKH.query.all()
    if request.method == "POST":
        try:
            ma_km = request.form.get("MaKM")
            noi_dung = request.form.get("NoiDung")
            thoigian = request.form.get("ThoiGian")
            bac_thanhvien = request.form.get("CapBacThanhVien")
            loai_tk = request.form.get("LoaiTKApDung")
            loai_km = request.form.get("LoaiKM")
            gia_tri_km = request.form.get("GiaTriKM")

            if not ma_km or not noi_dung or not thoigian or not loai_tk or not loai_km or not gia_tri_km:
                flash("Vui lòng nhập đầy đủ thông tin!", "danger")
                return redirect(url_for("home.them_uudai"), danh_sach_cap_bac=danh_sach_cap_bac)
            # Chuyển đổi thời gian về định dạng datetime
            thoigian = datetime.strptime(thoigian, "%Y-%m-%dT%H:%M")

            # Tạo đối tượng mới
            uu_dai = KhuyenMai(
                MaKM=ma_km,
                NoiDung=noi_dung,
                ThoiGian=thoigian,
                CapBacThanhVien=bac_thanhvien,
                LoaiTKApDung=loai_tk,
                LoaiKM=loai_km,
                GiaTriKM=float(gia_tri_km)
            )

            db.session.add(uu_dai)
            db.session.commit()
            flash("Thêm ưu đãi thành công!", "success")
            return redirect(url_for("home.admin_uudai"))

        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi thêm ưu đãi: {str(e)}", "danger")

    return render_template("admin/themUuDai.html", danh_sach_cap_bac=danh_sach_cap_bac)


@home_bp.route('/admin/xoa_uudai', methods=['POST'])
def xoa_uudai():
    # Lấy danh sách mã ưu đãi từ form
    uu_dai_ids = request.form.getlist("xoa_uu_dai")

    if not uu_dai_ids:
        flash("Vui lòng chọn ít nhất một ưu đãi để xóa.", "warning")
        return redirect(url_for('home.admin_uudai'))

    try:
        for maKM in uu_dai_ids:
            uu_dai = KhuyenMai.query.filter_by(MaKM=maKM).first()
            if uu_dai:
                db.session.delete(uu_dai)

        db.session.commit()
        flash("Xóa thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Lỗi khi xóa: " + str(e), "danger")

    return redirect(url_for('home.admin_uudai'))


@home_bp.route('/uudai/sua/<maKM>', methods=['GET', 'POST'])
def sua_uu_dai(maKM):
    uudai = KhuyenMai.query.get(maKM)
    if not uudai:
        flash('Không tìm thấy ưu đãi!', 'error')
        return redirect(url_for('home.admin_uudai'))

    if request.method == 'POST':
        # Lấy dữ liệu từ form (sửa tên trường để khớp với form)
        noi_dung = request.form.get('noi_dung')
        thoi_gian = request.form.get('thoi_gian')
        loai_tk_ap_dung = request.form.get('loai_tk_ap_dung')
        cap_bac_thanh_vien = request.form.get('cap_bac_thanh_vien')
        loai_km = request.form.get('loai_km')
        gia_tri_km = request.form.get('gia_tri_km')

        # Kiểm tra giá trị trước khi cập nhật
        if not thoi_gian:
            flash('Thời gian không được để trống!', 'error')
            return redirect(url_for('home.sua_uu_dai', maKM=maKM))

        try:
            # Cập nhật thông tin
            uudai.NoiDung = noi_dung
            uudai.ThoiGian = datetime.strptime(thoi_gian, '%Y-%m-%d').date()
            uudai.LoaiTKApDung = loai_tk_ap_dung
            # Xử lý trường nullable
            uudai.CapBacThanhVien = cap_bac_thanh_vien if cap_bac_thanh_vien else None
            uudai.LoaiKM = loai_km
            # Xử lý giá trị số
            uudai.GiaTriKM = int(gia_tri_km) if gia_tri_km else 0
            db.session.commit()
            flash('Cập nhật ưu đãi thành công!', 'success')
            return redirect(url_for('home.admin_uudai'))
        except ValueError as e:
            flash(
                'Định dạng thời gian không hợp lệ! Vui lòng nhập '
                + 'theo định dạng YYYY-MM-DD.', 'error')
            return redirect(url_for('home.sua_uu_dai', maKM=maKM))

    # Lấy danh sách loại tài khoản và cấp bậc để hiển thị trong dropdown
    loai_tk_list = LoaiTK.query.all()
    cap_bac_list = CapBacKH.query.all()
    return render_template('admin/suaUuDai.html', uudai=uudai,
                           loai_tk_list=loai_tk_list,
                           cap_bac_list=cap_bac_list)

# dia chi tra ve cho cac sidebar


@home_bp.route('/admin/khachhang')
def chinhsua_kh():
    return render_template('admin/chinhsuaKH.html')


@home_bp.route('/admin/uu_dai')
def chinhsua_uudai():
    return render_template('admin/chinhsuaUuDai.html')


@home_bp.route('/admin/capbac')
def chinhsua_capbac():
    return render_template('admin/chinhsuaCapBac.html')


@home_bp.route('/user/offers')
def xem_uudai():
    return render_template('user/offers.html')


# -------------------Quản lý cấp bậc-------------

# cap bac
@home_bp.route('/admin/xoa_capbac', methods=['POST'])
def xoa_capbac():
    # Lấy danh sách mã cap bac từ form
    capbac_ids = request.form.getlist("xoa_capbac")

    if not capbac_ids:
        flash("Vui lòng chọn ít nhất một cấp bậc để xóa.", "warning")
        return redirect(url_for('home.danh_sach_cap_bac'))

    try:
        for maCB in capbac_ids:
            capbac = CapBacKH.query.filter_by(MaCapBac=maCB).first()
            if capbac:
                db.session.delete(capbac)

        db.session.commit()
        flash("Xóa thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Lỗi khi xóa: " + str(e), "danger")

    return redirect(url_for('home.danh_sach_cap_bac'))


@home_bp.route('/admin/cap_bac')
def danh_sach_cap_bac():
    ten = loadTenNhanVien()
    cap_bac_list = CapBacKH.query.all()  # Lấy toàn bộ danh sách cấp bậc từ DB
    return render_template('admin/chinhsuaCapBac.html',
                           cap_bac_list=cap_bac_list, ten=ten)


@home_bp.route('/capbac/<maCB>')
def chi_tiet_cap_bac(maCB):
    capbac = CapBacKH.query.get(maCB)
    if not capbac:
        flash('Không tìm thấy cấp bậc!', 'error')
        return redirect(url_for('home.danh_sach_cap_bac'))
    return render_template('admin/chitietCapBac.html', capbac=capbac)


@home_bp.route("/them_capbac", methods=["GET", "POST"])
def them_capbac():
    if request.method == "POST":
        try:
            ma_cb = request.form.get("MaCapBac")
            ten_cb = request.form.get("TenCapBac")
            mucdatduoc = request.form.get("MucDatDuoc")

            if not ma_cb or not ten_cb or not mucdatduoc:
                flash("Vui lòng nhập đầy đủ thông tin!", "danger")
                return redirect(url_for("home.them_capbac"))
            # Lấy thời gian là ngày hôm nay
            ngaytao = datetime.today().date()
            # Tạo đối tượng mới
            capbac = CapBacKH(
                MaCapBac=ma_cb,
                TenCapBac=ten_cb,
                NgayTao=ngaytao,
                MucDatDuoc=Decimal(mucdatduoc)
            )

            db.session.add(capbac)
            db.session.commit()
            flash("Thêm cấp bậc thành công!", "success")
            return redirect(url_for("home.danh_sach_cap_bac"))

        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi thêm ưu đãi: {str(e)}", "danger")

    return render_template("admin/themCapBac.html")


@home_bp.route('/capbac/sua/<maCB>', methods=['GET', 'POST'])
def sua_cap_bac(maCB):
    capbac = CapBacKH.query.get(maCB)
    if not capbac:
        flash('Không tìm thấy cấp bậc!', 'error')
        return redirect(url_for('home.danh_sach_cap_bac'))

    if request.method == 'POST':
        # Lấy dữ liệu từ form (sửa tên trường để khớp với form)
        ten_capbac = request.form.get('ten_capbac')
        muc_dat_duoc = request.form.get('muc_dat_duoc')
        today = datetime.today().date()
        try:
            # Cập nhật thông tin
            capbac.TenCapBac = ten_capbac
            capbac.NgayTao = today
            capbac.MucDatDuoc = int(muc_dat_duoc) if muc_dat_duoc else 0
            db.session.commit()
            flash('Cập nhật cấp bậc thành công!', 'success')
            return redirect(url_for('home.danh_sach_cap_bac'))
        except ValueError as e:
            flash('Vui lòng nhập đầy đủ thông tin', 'error')
            return redirect(url_for('home.sua_capbac', maCB=maCB))

    return render_template('admin/suaCapBac.html', capbac=capbac)


@home_bp.route('/capbac/timkiem', methods=['GET'])
def tim_kiem_capbac():
    search_query = request.args.get(
        'search', '').strip()  # Lấy từ khóa tìm kiếm

    if search_query:
        cap_bac_list = CapBacKH.query.filter(
            CapBacKH.TenCapBac.ilike(f"%{search_query}%")).all()
    else:
        cap_bac_list = CapBacKH.query.all()

    return render_template('admin/chinhsuaCapBac.html', cap_bac_list=cap_bac_list, search_query=search_query)

# ## Tinh cap bac tu dong


def cap_nhat_cap_bac(ma_kh):
    """Kiểm tra và cập nhật cấp bậc khách hàng dựa trên điểm tích lũy"""
    lich_su = LichSuTichDiem.query.filter_by(MaKH=ma_kh).first()
    if not lich_su:
        return

    diem_tich_luy = lich_su.Diem
    cap_bac_moi = None

    # Lấy danh sách cấp bậc sắp xếp theo mức đạt được
    danh_sach_cap_bac = CapBacKH.query.order_by(CapBacKH.MucDatDuoc).all()

    for cap_bac in danh_sach_cap_bac:
        if diem_tich_luy >= cap_bac.MucDatDuoc:
            cap_bac_moi = cap_bac.MaCapBac
        else:
            break

    khach_hang = KhachHang.query.filter_by(MaKH=ma_kh).first()

    # Cập nhật nếu cần, KHÔNG commit ở đây
    if cap_bac_moi and khach_hang and khach_hang.MaCapBac != cap_bac_moi:
        khach_hang.MaCapBac = cap_bac_moi


def cap_nhat_diem_va_cap_bac(ma_tk: str, gia_tri_giao_dich: int):
    """Cập nhật điểm tích lũy và cấp bậc khách hàng dựa trên mã tài khoản và giá trị giao dịch"""
    tai_khoan = TaiKhoan.query.get(ma_tk)
    if not tai_khoan:
        return

    ma_kh = tai_khoan.MaKH
    lich_su = LichSuTichDiem.query.filter_by(MaKH=ma_kh).first()

    if not lich_su:
        lich_su = LichSuTichDiem(MaKH=ma_kh, ThoiGian=datetime.today(), Diem=0)
        db.session.add(lich_su)

    lich_su.Diem += gia_tri_giao_dich // 1000
    lich_su.ThoiGian = datetime.today()

    cap_nhat_cap_bac(ma_kh)

# Trí


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bank"
    )


def get_transaction_data(maTK, as_list=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(NgayGD, '%Y-%m') AS month,
               SUM(CASE WHEN ChieuGD=1 THEN GiaTriGD ELSE 0 END),
               SUM(CASE WHEN ChieuGD=0 THEN GiaTriGD ELSE 0 END)
        FROM lichsugiaodich
        WHERE TKGD = %s
        GROUP BY month
    """, (maTK,))

    results = cursor.fetchall()

    months = [row[0] for row in results]
    money_in = [float(row[1]) for row in results]
    money_out = [float(row[2]) for row in results]

    if as_list:
        cursor.execute(
            "SELECT MaGD, NgayGD, ChieuGD, GiaTriGD FROM lichsugiaodich WHERE TKGD = %s", (maTK,))

        all_tx = cursor.fetchall()
        transactions = [{"id": r[0], "NgayGD": r[1].strftime(
            "%Y-%m-%d"), "ChieuGD": r[2], "GiaTriGD": float(r[3])} for r in all_tx]
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


# mtri

@home_bp.route('/thongke')
def thongke():
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/thongke.html', isLogin=isLogin, tk=tk)


@home_bp.route('/sotietkiem')
def sotietkiem():
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/sotietkiem.html', tk=tk)


@home_bp.route('/lichsugiaodich')
def lichsugiaodich():
    isLogin = 'MaKH' in session
    maTK = session['MaTK'] if isLogin else None
    tk = TaiKhoan.query.get(maTK) if maTK else None
    return render_template('user/lichsugiaodich.html', tk=tk, isLogin=isLogin)


def generate_ma_tk():
    last = TaiKhoan.query.order_by(
        cast(func.substr(TaiKhoan.MaTK, 3), Integer).desc()
    ).first()
    if last and last.MaTK[2:].isdigit():
        maTK = f"TK{int(last.MaTK[2:]) + 1}"
    else:
        maTK = "TK1"
    return maTK


def generate_STK():
    while True:
        stk = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if not TaiKhoan.query.filter_by(STK=stk).first():
            return stk


@home_bp.route('/api/transactions')
def api_transactions():
    maTK = session['MaTK']

    return jsonify(get_transaction_data(maTK, as_list=True))


# biểu đồ chi tiêu (bieudochitieu.html)
@home_bp.route('/expense_chart_image')
def expense_chart_image():
    maTK = session['MaTK']
    data = (LichSuGiaoDich.query
            .with_entities(func.distinct(LichSuGiaoDich.HinhThuc), func.sum(LichSuGiaoDich.GiaTriGD))
            .filter(LichSuGiaoDich.TKGD == maTK)
            .group_by(LichSuGiaoDich.HinhThuc)
            .all())
    categories = [item[0] for item in data]
    expenses = [item[1] for item in data]

    fig, ax = plt.subplots()
    ax.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    img_io = io.BytesIO()
    fig.savefig(img_io, format='png', dpi=150, bbox_inches="tight")
    plt.close(fig)

    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@home_bp.route('/money_area_chart_image')
def money_area_chart_image():  # biểu đồ tiền vào ra (ở thongke)
    maTK = session['MaTK']
    data = get_transaction_data(maTK)
    months = data['months']
    money_in = data['money_in']
    money_out = data['money_out']

    total_in = sum(money_in)
    total_out = sum(money_out)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(months, money_in, color='#90CAF9',
                    alpha=0.5, label='Tiền Vào', linewidth=2)
    ax.fill_between(months, money_out, color='#FFCCBC',
                    alpha=0.5, label='Tiền Ra', linewidth=2)

    ax.plot(months, money_in, color='#42A5F5', linewidth=2)
    ax.plot(months, money_out, color='#FF7043', linewidth=2)

    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    ax.set_title('Biểu đồ Tiền Vào và Tiền Ra', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tháng', fontsize=12)
    ax.set_ylabel('Số Tiền (VND)', fontsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=10)

    ax.legend(frameon=False, fontsize=11)

    plt.figtext(0.5, -0.05,
                f"Tổng Thu: {total_in:,} VND    Tổng Chi: {total_out:,} VND",
                wrap=True, horizontalalignment='center', fontsize=12, color='black')

    img_io = io.BytesIO()
    plt.subplots_adjust(top=0.88, bottom=0.2)
    fig.savefig(img_io, format='png', dpi=150, bbox_inches="tight")
    plt.close(fig)

    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@home_bp.route('/mo-so-tiet-kiem', methods=['POST'])
def mo_so_tiet_kiem():
    maTK = session['MaTK']
    so_tien_gui = int(request.form['amount'])
    ky_han = request.form['term']

    taikhoan = TaiKhoan.query.filter_by(MaTK=maTK).first()
    if taikhoan is None:
        flash('Tài khoản không tồn tại!', 'error')
        return render_template('user/sotietkiem.html', taikhoan=taikhoan)

    if taikhoan.SoDu < so_tien_gui:
        flash('Số dư tài khoản không đủ!', 'error')
        return render_template('user/sotietkiem.html', taikhoan=taikhoan)

    # Trừ tiền
    taikhoan.SoDu -= so_tien_gui

    # Ngày mở và ngày kết thúc
    ngay_mo = date.today()
    if ky_han == '1 tháng':
        ngay_ket_thuc = ngay_mo + relativedelta(months=1)
        lai_suat = 3
    elif ky_han == '6 tháng':
        ngay_ket_thuc = ngay_mo + relativedelta(months=6)
        lai_suat = 4
    elif ky_han == '1 năm':
        ngay_ket_thuc = ngay_mo + relativedelta(years=1)
        lai_suat = 5
    else:
        ngay_ket_thuc = ngay_mo
        lai_suat = 0

    newtktietkiem = TaiKhoan(MaTK=generate_ma_tk(),
                             LoaiTK="ML2",
                             SoDu=so_tien_gui,
                             MaKH=taikhoan.MaKH,
                             STK=generate_STK(),
                             NgayDangKy=ngay_mo,
                             TrangThai=1,
                             ThoiGianDong=''
                             )

    # Tạo sổ tiết kiệm
    saving = SavingsSoTietKiem(
        MaKH=taikhoan.MaKH,
        SoTienGui=so_tien_gui,
        KyHan=ky_han,
        LaiSuat=lai_suat,
        NgayMo=ngay_mo,
        NgayKetThuc=ngay_ket_thuc
    )
    db.session.add(saving)
    db.session.add(newtktietkiem)
    db.session.commit()

    flash('Mở sổ tiết kiệm thành công!', 'success')
    return render_template('user/sotietkiem.html', taikhoan=taikhoan)


@home_bp.route('/tat_toan_sotietkiem', methods=['POST'])
def tat_toan_sotietkiem():
    # Lấy ID người dùng từ session
    makh = session['MaKH']
    matk = session['MaTK']
    if not makh or not matk:
        return redirect(url_for('home.tattoan'))

    # Tìm sổ tiết kiệm của người dùng kèm tài khoản
    sotk = SavingsSoTietKiem.query.filter_by(MaTK=matk).first()
    taikhoantietkiem = TaiKhoan.query.filter_by(MaTK=matk).first()
    if not sotk:
        flash('Không tìm thấy sổ tiết kiệm', 'error')
        return redirect(url_for('home.tattoan'))

    # Tìm tài khoản gốc (tài khoản thanh toán) của người dùng
    taikhoan = TaiKhoan.query.filter_by(MaKH=makh, MaTK=sotk.MaTKNguon).first()
    if not taikhoan:

        return redirect(url_for('home.sotietkiem'))
    if sotk.NgayKetThuc > date.today():
        flash("Chưa đến ngày tất toán!", 'warning')
        # hoặc redirect
        return render_template('user/tattoan.html', sotietkiem=sotk)
    else:
        # lai suat
        laisuat = sotk.SoTienGui * (1 + sotk.kyhan.LaiSuat / 100)
        # Cộng số dư từ sổ tiết kiệm vào tài khoản gốc
        taikhoan.SoDu += laisuat

        # cập nhật lsgd
        lsgd = LichSuGiaoDich(
            MaGD=generate_ma_gd(),
            NgayGD=date.today(),
            ChieuGD=1,
            NoiDungGD="Tất toán sổ tiết kiệm",
            GiaTriGD=laisuat,
            HinhThuc="Tất toán sổ tiết kiệm",
            TKGD=sotk.MaTKNguon
        )

        # Xoá sổ tiết kiệm
        db.session.delete(sotk)
        db.session.delete(taikhoantietkiem)
        db.session.add(lsgd)
        cap_nhat_diem_va_cap_bac(lsgd.TKGD, int(laisuat))

        db.session.commit()
        flash('Tất toán thành công. Tài khoản đã đóng.', 'success')
        return redirect(url_for('account.chooseAcc'))


def generate_ma_gd():
    # Lấy ls có mã lớn nhất theo số sau "GD"
    last_gd = LichSuGiaoDich.query.order_by(
        db.cast(db.func.substr(LichSuGiaoDich.MaGD, 3), db.Integer).desc()
    ).first()

    if last_gd:
        # Trích số nguyên sau "KH"
        last_id = int(last_gd.MaGD[2:])
        new_id = f"GD{last_id + 1}"
    else:
        new_id = "GD1"

    return new_id


@home_bp.route('/tattoan')
def tattoan():
    matk = session['MaTK']
    sotietkiem = SavingsSoTietKiem.query.filter_by(MaTK=matk).first()
    return render_template('user/tattoan.html', sotietkiem=sotietkiem)
