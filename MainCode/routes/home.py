
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import db, TaiKhoan, KhachHang, CapBacKH, LoaiTK, KhuyenMai, LichSuGiaoDich, AccountKH
from datetime import datetime, date
from decimal import Decimal
import re

from models import db, TaiKhoan, KhachHang, CapBacKH, LoaiTK, KhuyenMai, LichSuGiaoDich, LichSuTichDiem, NhanVien
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import or_
from sqlalchemy import event
from sqlalchemy.sql import func

home_bp = Blueprint('home', __name__)


# Kiểm tra xem đã chọn tại khoản chưa
@home_bp.route('/home')
def home():
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))

    maTK = session['MaTK']
    tk = TaiKhoan.query.get(maTK)
    return render_template('user/home.html', tk=tk)


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
    return render_template('user/infoUser.html', info=info, infoCard=infoCard)


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
    return render_template('user/changeInfoUser.html', info=info)

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
            # hoten = request.form.get('hoten')
            # cccd = request.form.get('cccd')
            # noicapcccd = request.form.get('noicapcccd')
            # quoctich = request.form.get('quoctich')
            # noicutru = request.form.get('noicutru')
            # diachithuongtru = request.form.get('diachithuongtru')
            # sodienthoai = request.form.get('sodienthoai')
            # email = request.form.get('email')
            # ngaysinh = request.form.get('ngaysinh')
            # ngaycapcccd = request.form.get('ngaycapcccd')
            # cogiatriden = request.form.get('cogiatriden')
            # dantoc = request.form.get('dantoc')
            # diachihientai = request.form.get('diachihientai')
            # gioitinh = request.form.get('gioitinh')
            # nghenghiep = request.form.get('nghenghiep')
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


def validate_input(data):
    errors = {}

    for field, (pattern, error_msg) in patterns.items():
        value = data.get(field, "").strip()
        if not pattern.match(value):
            errors[field] = error_msg  # Lưu thông báo lỗi nếu không khớp regex

    return errors  # Trả về dict lỗi, rỗng nếu không có lỗi

# ------------Quản lý khách Hàng-----------------


@home_bp.route('/admin/khachhang')
def admin_khachhang():

    tai_khoan_list = TaiKhoan.query.all()  # Lấy tất cả khách hàng từ database
    return render_template('admin/chinhsuaKH.html', tai_khoan_list=tai_khoan_list)


@home_bp.route('/khachhang/timkiem', methods=['GET'])
def tim_kiem_khachhang():
    search_query = request.args.get(
        'search', '').strip()  # Lấy từ khóa tìm kiếm

    if search_query:
        khach_hang_list = KhachHang.query.filter(
            KhachHang.HoTen.ilike(f"%{search_query}%")).all()
    else:
        khach_hang_list = KhachHang.query.all()
    for khach_hang in khach_hang_list:
        tai_khoan_list = [
            tk for kh in khach_hang_list for tk in TaiKhoan.query.filter_by(MaKH=kh.MaKH).all()]

    return render_template('admin/chinhsuaKH.html', tai_khoan_list=tai_khoan_list, search_query=search_query)


@home_bp.route('/khachhang/<maKH>')
def chi_tiet_khachhang(maKH):
    khach_hang = KhachHang.query.get(maKH)
    if not khach_hang:
        flash('Không tìm thấy khách hàng!', 'error')
        return redirect(url_for('home.admin_khachhang'))
    return render_template('admin/chitietKH.html', khach_hang=khach_hang)


def generate_ma_kh():
    # Lấy khách hàng có mã lớn nhất
    last_kh = KhachHang.query.order_by(KhachHang.MaKH.desc()).first()

    if last_kh:
        last_id = int(last_kh.MaKH[2:])  # Lấy số từ KH001 -> 001 -> 1
        # Tăng lên 1, format thành KH002, KH003, ...
        new_id = f"KH{last_id + 1:03d}"
    else:
        new_id = "KH001"  # Nếu chưa có khách hàng nào

    return new_id


@home_bp.route("/them_khachhang", methods=["GET", "POST"])
def them_khachhang():
    if request.method == "POST":
        try:
            ma_kh = generate_ma_kh()  # 🔥 Tự động sinh MaKH
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

            ma_nvql = "NV1"  # 🔥 Mặc định là NV1
            ma_cap_bac = "CB1"  # 🔥 Mặc định là CB1
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
            return redirect(url_for("home.chinhsua_khachhang", maKH=ma_kh))

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
    ma_tk = session['MaTK']

    user = KhachHang.query.get(ma_kh)

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
    return render_template('user/offers.html', uu_dai_list=uu_dai_list, current_date=today)


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
            return redirect(url_for("home.chinhsua_uudai"))

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
        return redirect(url_for('home.chinhsua_uudai'))

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

    return redirect(url_for('home.chinhsua_uudai'))


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
            return redirect(url_for("home.chinhsua_capbac"))

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

    # Nếu không có lịch sử tích điểm, thoát ra.
    if not lich_su:
        return

    diem_tich_luy = lich_su.Diem
    cap_bac_moi = None

    # Lấy danh sách cấp bậc sắp xếp theo mức đạt được
    danh_sach_cap_bac = CapBacKH.query.order_by(CapBacKH.MucDatDuoc).all()

    # Duyệt qua từng cấp bậc để tìm cấp bậc thích hợp
    for cap_bac in danh_sach_cap_bac:
        if diem_tich_luy >= cap_bac.MucDatDuoc:
            cap_bac_moi = cap_bac.MaCapBac
        else:
            break  # Dừng lại khi điểm tích lũy không đủ cho cấp bậc tiếp theo
    khach_hang = KhachHang.query.filter_by(MaKH=ma_kh).first()
    # Nếu cấp bậc mới được tìm thấy và khác với cấp bậc hiện tại
    if cap_bac_moi:
        if khach_hang and khach_hang.MaCapBac != cap_bac_moi:
            khach_hang.MaCapBac = cap_bac_moi
            db.session.commit()


@event.listens_for(LichSuGiaoDich, 'after_insert')
def after_insert_lich_su_giao_dich(mapper, connection, target):
    """ Cập nhật điểm tích lũy và cấp bậc khách hàng khi có giao dịch mới """
    tai_khoan = TaiKhoan.query.filter_by(MaTK=target.TKGD).first()

    if tai_khoan:
        lich_su = LichSuTichDiem.query.filter_by(MaKH=tai_khoan.MaKH).first()

        # Nếu không có lịch sử tích điểm, tạo mới
        if not lich_su:
            lich_su = LichSuTichDiem(MaKH=tai_khoan.MaKH, Diem=0)
            db.session.add(lich_su)

        # Tính toán điểm tích lũy từ giá trị giao dịch
        # Mỗi 1000 đơn vị giao dịch tương ứng với 1 điểm
        lich_su.Diem += target.GiaTriGD // 1000

        # Commit thay đổi điểm tích lũy
        db.session.commit()

        # Cập nhật cấp bậc sau khi điểm thay đổi
        cap_nhat_cap_bac(tai_khoan.MaKH)
