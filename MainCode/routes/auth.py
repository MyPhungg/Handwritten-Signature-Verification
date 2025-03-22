from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import accountKH
import os
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        account = accountKH.query.filter_by(
            TenDangNhap=username, MatKhau=password).first()
        if account:
            session['MaKH'] = account.MaKH
            return redirect(url_for('account.chooseAcc'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')

    print("Current Working Directory:", os.getcwd())
    print("Template Folder Path:", os.path.abspath("templates"))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('MaKH', None)
    session.pop('MaTK', None)
    flash('Bạn đã đăng xuất!', 'success')
    return redirect(url_for('auth.login'))
