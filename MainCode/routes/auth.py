from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import AccountKH, KhachHang, AccountNV
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kiểm tra tài khoản khách hàng
        user_kh = AccountKH.query.filter_by(TenDangNhap=username, MatKhau=password).first()
        if user_kh:
            session['MaKH'] = user_kh.MaKH
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('home.home'))
        
        # Kiểm tra tài khoản nhân viên (admin)
        user_nv = AccountNV.query.filter_by(TenDangNhap=username, MatKhau=password).first()
        if user_nv:
            session['MaNV'] = user_nv.MaNV
            flash('Đăng nhập admin thành công!', 'success')
            return redirect(url_for('home.admin_uudai'))
        
        flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('MaKH', None)
    session.pop('MaTK', None)
    flash('Bạn đã đăng xuất!', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/login/forgetAcc', methods=['GET'])
def forgetAcc():
    return render_template('forgetAcc.html')


@auth_bp.route('/login/forgetAcc/submit', methods=['GET', 'POST'])
def forgetAccSubmit():
    if request.method == 'POST':
        soDienThoai = request.form.get('phonenumber')
        authMethod = request.form.get('authMethod')
        cccd = request.form.get('cccd')
        khachHang = KhachHang.query.filter_by(SoDienThoai=soDienThoai).first()
        if not khachHang:
            flash('Không có tài khoản nào liên kết với '
                  'số điện thoại vừa nhập!', 'error')
            return redirect(url_for('auth.forgetAcc'))
        if authMethod == 'cccd':
            if khachHang.SoCCCD == cccd:
                tenDN = AccountKH.query.filter_by(
                    MaKH=khachHang.MaKH).first()
                if not tenDN:
                    flash('Lỗi trong việc tìm kiếm mã KH hoặc tên ĐN', 'error')
                    return redirect(url_for('auth.forgetAcc'))
                else:
                    return render_template('forgetAcc.html',
                                           soDienThoai=soDienThoai,
                                           username=tenDN.TenDangNhap,
                                           show_result=True)
            else:
                flash('Số CCCD không khớp!', 'error')
                return redirect(url_for('auth.forgetAcc'))
        if authMethod == 'signature':
            flash("Chưa hỗ trợ tính năng này!", 'error')
            return redirect(url_for('auth.forgetAcc'))
        # Nếu không chọn hình thức xác thực
        else:
            flash('Vui lòng chọn hình thức xác thực!', 'error')
            return redirect(url_for('auth.forgetAcc'))
