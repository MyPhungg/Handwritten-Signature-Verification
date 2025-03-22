from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import taiKhoan

account_bp = Blueprint('account', __name__)


@account_bp.route('/login/chooseAcc', methods=['GET', 'POST'])
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
    dsTaiKhoan = taiKhoan.query.filter_by(MaKH=maKH).all()
    return render_template('chooseAcc.html', dsTaiKhoan=dsTaiKhoan)
