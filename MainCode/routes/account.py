from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import TaiKhoan
from models import LoaiTK, db
import random
from datetime import datetime

account_bp = Blueprint('account', __name__)

# Chọn acc


@account_bp.route('/chooseAcc', methods=['GET', 'POST'])
def chooseAcc():
    if 'MaKH' not in session:
        flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        selected_MaTK = request.form.get('taikhoan')
        if selected_MaTK:
            session['MaTK'] = selected_MaTK
            return redirect(url_for('home.home'))
        else:
            flash('Vui lòng chọn một tài khoản!', 'error')

    maKH = session['MaKH']
    # Lấy danh sách tài khoản kèm thông tin LoaiTK
    dsTaiKhoan = (
        TaiKhoan.query
        .join(LoaiTK, TaiKhoan.LoaiTK == LoaiTK.MaLoai)
        .filter(TaiKhoan.MaKH == maKH)
        .with_entities(
            TaiKhoan.MaTK,
            TaiKhoan.SoDu,
            LoaiTK.TenLoai
        )
        .all()
    )
    return render_template('chooseAcc.html', dsTaiKhoan=dsTaiKhoan)

# tạo số tài khoản


def generate_account_number(length=12):
    account_number = ''.join(random.choices('0123456789', k=length))
    return account_number


@account_bp.route('/taoAccMoi', methods=['POST', 'GET'])
def taoTaiKhoan():
    if request.method == 'POST':
        # Đếm số lượng nhân viên hiện có
        so_luong_tai_khoan = TaiKhoan.query.count()
        maTK = f"TK{so_luong_tai_khoan + 1}"

        maKH = session['MaKH']
        soTaiKhoan = request.form['SoTaiKhoan']
        maLoaiTK = request.form['maLoaiTK']
        soDu = 0
        ngayDangKy = (datetime.now()).strftime("%Y-%m-%d %H-%M-%S")
        taiKhoanMoi = TaiKhoan(
            MaTK=maTK,
            LoaiTK=maLoaiTK,
            SoDu=soDu,
            MaKH=maKH,
            STK=soTaiKhoan,
            NgayDangKy=ngayDangKy,
            TrangThai=1)
        db.session.add(taiKhoanMoi)
        db.session.commit()
        return redirect(url_for('account.chooseAcc'))
    SoTaiKhoan = generate_account_number()
    dsLoaiTK = LoaiTK.query.filter(LoaiTK.MaLoai != 'ML2').all()

    return render_template('user/taoAccMoi.html', SoTaiKhoan=SoTaiKhoan, dsLoaiTK=dsLoaiTK)
