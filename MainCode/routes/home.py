from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import taiKhoan

home_bp = Blueprint('home', __name__)


@home_bp.route('/home')
def home():
    if 'MaTK' not in session:
        flash('Vui lòng chọn tài khoản trước!', 'error')
        return redirect(url_for('account.chooseAcc'))

    maTK = session['MaTK']
    tk = taiKhoan.query.get(maTK)
    return render_template('home.html', tk=tk)
