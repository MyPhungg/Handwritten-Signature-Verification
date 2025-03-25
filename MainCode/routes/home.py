from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import db, TaiKhoan, KhachHang, CapBacKH, LoaiTK, KhuyenMai, LichSuGiaoDich, AccountKH
from datetime import datetime,date
from decimal import Decimal
#from sqlalchemy.sql import func
#from apscheduler.schedulers.background import BackgroundScheduler
home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))

    maTK = session['MaTK']
    tk = TaiKhoan.query.get(maTK)
    return render_template('user/home.html', tk=tk)

@home_bp.route('/infoUser')
def inforUser():
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
# uu dai
@home_bp.route('/uudai')
def xem_uudai():
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'MaKH' not in session:
        flash('Vui lòng đăng nhập để xem ưu đãi!', 'error')
        return redirect(url_for('auth.login'))

    # Lấy thông tin khách hàng từ session
    ma_kh = session['MaKH']
    user = KhachHang.query.get(ma_kh)
    if not user:
        flash('Không tìm thấy thông tin khách hàng!', 'error')
        session.pop('MaKH', None)
        return redirect(url_for('auth.login'))

    # Lấy tài khoản đăng nhập của khách hàng
    account_kh = AccountKH.query.get(ma_kh)
    if not account_kh:
        flash('Không tìm thấy tài khoản đăng nhập của bạn!', 'error')
        return redirect(url_for('home.home'))

    # Lấy danh sách tất cả tài khoản ngân hàng của khách hàng
    tai_khoan_list = TaiKhoan.query.filter_by(MaKH=account_kh.MaKH).all()
    if not tai_khoan_list:
        flash('Không tìm thấy tài khoản ngân hàng nào của bạn!', 'error')
        return redirect(url_for('home.home'))

    # Lấy danh sách các loại tài khoản của khách hàng
    loai_tk_list = [tai_khoan.LoaiTK for tai_khoan in tai_khoan_list]

    # Lọc ưu đãi dựa trên LoaiTKApDung và CapBacThanhVien
    uu_dai_list = KhuyenMai.query.filter(
        (KhuyenMai.LoaiTKApDung.in_(loai_tk_list)) &
        ((KhuyenMai.CapBacThanhVien == user.MaCapBac) | (KhuyenMai.CapBacThanhVien == None))
    ).all()

    # Lấy ngày hiện tại
    current_date = date.today()
    return render_template('user/offers.html', uu_dai_list=uu_dai_list, current_date=current_date)

@home_bp.route('/uudai/<maKM>')
def chi_tiet_uudai(maKM):
    uu_dai = KhuyenMai.query.get(maKM)
    if not uu_dai:
        flash('Không tìm thấy ưu đãi!', 'error')
        return redirect(url_for('home.danh_sach_uudai'))
    return render_template('admin/chitietUuDai.html', uu_dai=uu_dai)

@home_bp.route('/uudai/timkiem', methods=['GET'])
def tim_kiem_uudai():
    keyword = request.args.get('keyword', '')
    uu_dai_list = KhuyenMai.query.filter(KhuyenMai.NoiDung.contains(keyword)).all()
    return render_template('user/offers.html', uu_dai_list=uu_dai_list, keyword=keyword)

@home_bp.route('/admin/uudai')
def admin_uudai():
    uu_dai_list = KhuyenMai.query.all()  # Lấy tất cả ưu đãi từ CSDL
    return render_template('admin/chinhsuaUuDai.html', uu_dai_list=uu_dai_list)

@home_bp.route("/them_uudai", methods=["GET", "POST"])
def them_uudai():
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
                return redirect(url_for("home.them_uudai"))
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

    return render_template("admin/themUuDai.html")

@home_bp.route('/admin/xoa_uudai', methods=['POST'])
def xoa_uudai():
    uu_dai_ids = request.form.getlist("xoa_uu_dai")  # Lấy danh sách mã ưu đãi từ form

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
            uudai.CapBacThanhVien = cap_bac_thanh_vien if cap_bac_thanh_vien else None  # Xử lý trường nullable
            uudai.LoaiKM = loai_km
            uudai.GiaTriKM = int(gia_tri_km) if gia_tri_km else 0  # Xử lý giá trị số
            db.session.commit()
            flash('Cập nhật ưu đãi thành công!', 'success')
            return redirect(url_for('home.admin_uudai'))
        except ValueError as e:
            flash('Định dạng thời gian không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.', 'error')
            return redirect(url_for('home.sua_uu_dai', maKM=maKM))

    # Lấy danh sách loại tài khoản và cấp bậc để hiển thị trong dropdown
    loai_tk_list = LoaiTK.query.all()
    cap_bac_list = CapBacKH.query.all()
    return render_template('admin/suaUuDai.html', uudai=uudai, loai_tk_list=loai_tk_list, cap_bac_list=cap_bac_list)

# dia chi tra ve cho cac sidebar
@home_bp.route('/admin/khachhang')
def chinhsua_kh():
    return render_template('admin/chinhsuaKH.html')

@home_bp.route('/admin/uudai')
def chinhsua_uudai():
    return render_template('admin/chinhsuaUaDai.html')

@home_bp.route('/admin/capbac')
def chinhsua_capbac():
    return render_template('admin/chinhsuaCapBac.html')

@home_bp.route('/user/offers')
def xem_uudai():
    return render_template('user/offers.html')

# cap bac
@home_bp.route('/admin/capbac')
def danh_sach_cap_bac():
    cap_bac_list = CapBacKH.query.all()  # Lấy toàn bộ danh sách cấp bậc từ DB
    return render_template('admin/chinhsuaCapBac.html', cap_bac_list=cap_bac_list)

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

            if not ma_cb or not ten_cb or not mucdatduoc :
                flash("Vui lòng nhập đầy đủ thông tin!", "danger")
                return redirect(url_for("home.them_capbac"))
            # Lấy thời gian là ngày hôm nay
            ngaytao = datetime.today().date()
            # Tạo đối tượng mới
            capbac= CapBacKH(
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
        # Lấy dữ liệu từ form
        ten_cap_bac = request.form.get('ten_cap_bac')
        muc_dat_duoc = request.form.get('muc_dat_duoc')
        mo_ta = request.form.get('mo_ta')

        # Cập nhật thông tin
        capbac.TenCapBac = ten_cap_bac
        capbac.MucDatDuoc = muc_dat_duoc
        db.session.commit()
        flash('Cập nhật cấp bậc thành công!', 'success')
        return redirect(url_for('home.danh_sach_cap_bac'))

    return render_template('admin/suaCapBac.html', capbac=capbac)

## Tinh cap bac tu dong

###def nang_cap_cap_bac():
    print(f"Bắt đầu nâng cấp cấp bậc khách hàng: {datetime.now()}")
    
    # Lấy danh sách tất cả khách hàng
    khach_hangs = KhachHang.query.all()
    
    # Lấy danh sách cấp bậc, sắp xếp theo MucDatDuoc tăng dần
    cap_bacs = CapBacKH.query.order_by(CapBacKH.MucDatDuoc.asc()).all()
    
    for khach_hang in khach_hangs:
        # Lấy danh sách tài khoản của khách hàng
        tai_khoans = TaiKhoan.query.filter_by(MaKH=khach_hang.MaKH).all()
        if not tai_khoans:
            print(f"Khách hàng {khach_hang.MaKH} không có tài khoản.")
            continue
        
        # Tính tổng chi tiêu từ bảng LichSuGiaoDich
        # Chỉ tính các giao dịch có ChieuGD = 1 (chi tiêu)
        tong_chi_tieu = 0
        for tai_khoan in tai_khoans:
            # Tính tổng GiaTriGD cho từng tài khoản
            tong = db.session.query(func.sum(LichSuGiaoDich.GiaTriGD)).filter(
                LichSuGiaoDich.TKGD == tai_khoan.MaTK,
                LichSuGiaoDich.ChieuGD == 1
            ).scalar() or 0
            tong_chi_tieu += tong
        
        # Tìm cấp bậc phù hợp
        cap_bac_phu_hop = None
        for cap_bac in cap_bacs:
            if tong_chi_tieu >= cap_bac.MucDatDuoc:
                cap_bac_phu_hop = cap_bac
            else:
                break  # Vì danh sách đã sắp xếp tăng dần, nên thoát khi không thỏa mãn
        
        # Cập nhật cấp bậc cho khách hàng
        if cap_bac_phu_hop:
            if khach_hang.MaCapBac != cap_bac_phu_hop.MaCapBac:
                khach_hang.MaCapBac = cap_bac_phu_hop.MaCapBac
                print(f"Khách hàng {khach_hang.MaKH} được nâng cấp lên {cap_bac_phu_hop.TenCapBac} (Tổng chi tiêu: {tong_chi_tieu})")
        else:
            khach_hang.MaCapBac = None  # Không đạt cấp bậc nào
            print(f"Khách hàng {khach_hang.MaKH} không đạt cấp bậc nào (Tổng chi tiêu: {tong_chi_tieu})")
    
    # Lưu thay đổi vào CSDL
    try:
        db.session.commit()
        print(f"Kết thúc nâng cấp cấp bậc khách hàng: {datetime.now()}")
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi nâng cấp cấp bậc: {e}")
    ###