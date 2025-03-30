from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import AccountKH, KhachHang, AccountNV, NhanVien
auth_bp = Blueprint('auth', __name__)

# Đăng nhập


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        account = AccountKH.query.filter_by(
            TenDangNhap=username, MatKhau=password).first()
        if account:
            session['MaKH'] = account.MaKH
            session['user_type'] = 'KH'  # Lưu loại người dùng vào session
            return redirect(url_for('account.chooseAcc'))

        # Kiểm tra xem có phải là nhân viên không
        account_nv = AccountNV.query.filter_by(
            TenDangNhap=username, MatKhau=password).first()
        if account_nv:
            session['MaNV'] = account_nv.MaNV
            session['user_type'] = 'NV'  # Lưu loại người dùng vào session
            return redirect(url_for('home.admin_uudai'))

        flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
    return render_template('login.html')

# Đăng xuất


@auth_bp.route('/logout')
def logout():
    session.pop('MaKH', None)
    session.pop('MaTK', None)
    flash('Bạn đã đăng xuất!', 'success')
    return redirect(url_for('auth.login'))

# Chuyển hướng tới trang quên tài khoản


@auth_bp.route('/login/forgetAcc', methods=['GET'])
def forgetAcc():
    return render_template('forgetAcc.html')

# Xử lý quên tài khoản


def process_forgot_account(soDienThoai, cccd, authMethod):
    # Danh sách các model để kiểm tra
    user_models = [(KhachHang, AccountKH, "MaKH"),
                   (NhanVien, AccountNV, "MaNV")]
    user, account_model, account_key = None, None, None

    # Kiểm tra lần lượt trong các bảng
    for model, acc_model, key in user_models:
        user = model.query.filter_by(SoDienThoai=soDienThoai).first()
        if user:
            account_model, account_key = acc_model, key
            break

    # Nếu không tìm thấy user
    if not user:
        flash('Không có tài khoản nào liên kết với số điện thoại vừa nhập!', 'error')
        return render_template('forgetAcc.html', soDienThoai=soDienThoai)

    # Xác thực theo CCCD
    if authMethod == 'cccd':
        if user.SoCCCD == cccd:
            account = account_model.query.filter_by(
                **{account_key: getattr(user, account_key)}).first()
            if not account:
                flash('Lỗi trong việc tìm kiếm tài khoản', 'error')
                return render_template('forgetAcc.html', soDienThoai=soDienThoai)

            return render_template('forgetAcc.html',
                                   soDienThoai=soDienThoai,
                                   username=account.TenDangNhap,
                                   show_result=True)
        else:
            flash('Số CCCD không khớp!', 'error')
            return render_template('forgetAcc.html', soDienThoai=soDienThoai)

    # Xác thực bằng chữ ký (chưa hỗ trợ)
    if authMethod == 'signature':
        flash("Chưa hỗ trợ tính năng này!", 'error')
        return render_template('forgetAcc.html', soDienThoai=soDienThoai)

    # Nếu không chọn hình thức xác thực
    flash('Vui lòng chọn hình thức xác thực!', 'error')
    return render_template('forgetAcc.html', soDienThoai=soDienThoai)


@auth_bp.route('/login/forgetAcc/submit', methods=['GET', 'POST'])
def forgetAccSubmit():
    if request.method == 'POST':
        soDienThoai = request.form.get('phonenumber')
        authMethod = request.form.get('authMethod')
        cccd = request.form.get('cccd')
        return process_forgot_account(soDienThoai, cccd, authMethod)

# Chuyển hướng tới trang quên mật khẩu


@auth_bp.route('/login/forgetPass', methods=['GET'])
def forgetPass():
    return render_template('forgetPass.html')

# Xử lý quên mật khẩu


def process_forgot_password(username, cccd, authMethod):
    # Tìm trong bảng Khách Hàng trước
    account = AccountKH.query.filter_by(TenDangNhap=username).first()
    account_model = KhachHang
    account_key = "MaKH"

    # Nếu không tìm thấy trong Khách Hàng, thử tìm trong Nhân Viên
    if not account:
        account = AccountNV.query.filter_by(TenDangNhap=username).first()
        account_model = NhanVien
        account_key = "MaNV"

    # Nếu không tìm thấy cả hai thì báo lỗi
    if not account:
        flash('Không có tài khoản!', 'error')
        return render_template('forgetPass.html', username=username)
    user = account_model.query.filter_by(
        **{account_key: getattr(account, account_key)}).first()
    # Xác thực theo CCCD
    if authMethod == 'cccd':
        if user.SoCCCD == cccd:
            password = account.MatKhau
            if not password:
                flash('Lỗi trong việc tìm kiếm mã KH hoặc mật khẩu',
                      'error')
                return render_template('forgetPass.html', username=username)
            else:
                return render_template('forgetPass.html',
                                       username=username,
                                       password=password,
                                       show_result=True)
        else:
            flash('Số CCCD không khớp!', 'error')
            return render_template('forgetPass.html', username=username)

    # Xác thực bằng chữ ký (chưa hỗ trợ)
    if authMethod == 'signature':
        flash("Chưa hỗ trợ tính năng này!", 'error')
        return render_template('forgetPass.html', username=username)

    # Nếu không chọn hình thức xác thực
    flash('Vui lòng chọn hình thức xác thực!', 'error')
    return render_template('forgetPass.html', username=username)


@auth_bp.route('/login/forgetPass/submit', methods=['GET', 'POST'])
def forgetPassSubmit():
    if request.method == 'POST':
        username = request.form.get('username')
        authMethod = request.form.get('authMethod')
        cccd = request.form.get('cccd')
        return process_forgot_password(username, cccd, authMethod)

# Đang suy nghĩ nên chỉnh CSDL để xét trường hợp Nhân viên
