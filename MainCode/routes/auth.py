from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import AccountKH, KhachHang, AccountNV
auth_bp = Blueprint('auth', __name__)
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from werkzeug.utils import secure_filename



# Load mô hình chữ ký
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.abspath(
    os.path.join(current_dir, '..', '..', 'Handwritten_Signature_Verification', 'my_model.keras')
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
    upload_path = os.path.join(current_dir, '..', '..', 'Handwritten_Signature_Verification', 'my_model.keras')
    file.save(upload_path)

    # Tiền xử lý và dự đoán
    image_array = preprocess_image(upload_path)
    prediction = model.predict(image_array)[0][0]

    # Gán nhãn và confidence
    label = "Thật" if prediction >= 0.5 else "Giả"
    confidence = round(float(prediction if prediction >= 0.5 else 1 - prediction) * 100, 2)

    return label, confidence


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