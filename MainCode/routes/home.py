from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import TaiKhoan, KhachHang, CapBacKH, LoaiTK

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


# @home_bp.route('/infoUser/changeInfoUser')
# def changeInfoUser():
