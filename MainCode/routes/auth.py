from werkzeug.utils import secure_filename
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import AccountKH, KhachHang, AccountNV, NhanVien
auth_bp = Blueprint('auth', __name__)


# Load mô hình chữ ký
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.abspath(
    os.path.join(current_dir, '..', '..',
                 'Handwritten_Signature_Verification', 'model.h5')  # my_model.keras
)
model = load_model(model_path)

# Hàm xử lý tiền ảnh


def preprocess_image(image_path):
    img = Image.open(image_path).convert("L")  # grayscale
    img = img.resize((128, 128))               # resize
    img_array = np.array(img) / 255.0          # normalize
    img_array = img_array.reshape(1, 128, 128, 1)
    return img_array

# Hàm xử lý chữ ký thật hoặc giả


def verify_signature(file):
    # Lưu ảnh tạm thời
    filename = secure_filename(file.filename)
    upload_path = os.path.join(
        current_dir, '..', '..', 'Handwritten_Signature_Verification', 'my_model.keras')
    file.save(upload_path)

    # Tiền xử lý và dự đoán
    image_array = preprocess_image(upload_path)
    prediction = model.predict(image_array)[0][0]

    # Gán nhãn và confidence
    label = "Thật" if prediction >= 0.5 else "Giả"
    confidence = round(float(prediction if prediction >=
                       0.5 else 1 - prediction) * 100, 2)

    return label, confidence

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
        if username == 'admin' and password == 'admin':
            session['user_type'] = 'admin'
            return redirect(url_for('admin.loadDanhSachNhanVien'))
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


@auth_bp.route('/predict', methods=['POST'])
def predict_signature():
    if 'signature' not in request.files:
        flash('Không tìm thấy ảnh chữ ký!', 'error')
        return redirect(request.referrer)

    file = request.files['signature']
    if file.filename == '':
        flash('Chưa chọn file!', 'error')
        return redirect(request.referrer)

    label, confidence = verify_signature(file)
    flash(f'Chữ ký được xác định là: {label} ({confidence}%)', 'success')
    return render_template('verify_result.html', label=label, confidence=confidence)


@auth_bp.route('/test-signature', methods=['GET'])
def test_signature_page():
    return render_template('test_signature.html')


@auth_bp.route('/api/predict', methods=['POST'])
def api_predict_signature():
    if 'signature' not in request.files:
        return {'error': 'Không tìm thấy ảnh chữ ký!'}, 400

    file = request.files['signature']
    if file.filename == '':
        return {'error': 'Chưa chọn file!'}, 400

    label, confidence = verify_signature(file)
    return {'label': label, 'confidence': confidence}
