from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import TaiKhoan
from models import LoaiTK

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
