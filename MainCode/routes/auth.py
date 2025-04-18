from werkzeug.utils import secure_filename
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import os
import vc2
from flask import Blueprint, render_template, request, redirect, url_for
from flask import session, flash
from models import AccountKH, KhachHang, AccountNV, NhanVien
auth_bp = Blueprint('auth', __name__)
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity


base_model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Handwritten_Signature_Verification')
with open(os.path.join(base_model_path, "model.json"), "r") as json_file:
    model = model_from_json(json_file.read())

model.load_weights(os.path.join(base_model_path, "model.weights.h5"))


# Tạo intermediate_layer_model giống phần huấn luyện:
# Mô hình dùng để trích đặc trưng phải lấy đầu ra từ lớp áp chót (Dense(256)):
intermediate_layer_model = Model(inputs=model.input, outputs=model.layers[-2].output)

# Hàm tiền xử lý ảnh chuẩn với VGG16:
def extract_features(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)

    features = intermediate_layer_model.predict(image)
    return features


# Duyệt toàn bộ data
dataset_root = os.path.join(os.path.dirname(__file__), '..', '..', 'Handwritten_Signature_Verification', 'Dataset')

real_paths = []
forge_paths = []

for folder_name in sorted(os.listdir(dataset_root)):
    folder_path = os.path.join(dataset_root, folder_name)
    if os.path.isdir(folder_path):
        real_dir = os.path.join(folder_path, 'real')
        forge_dir = os.path.join(folder_path, 'forge')

        # Lấy danh sách ảnh thật và giả
        if os.path.exists(real_dir):
            for img in os.listdir(real_dir):
                real_paths.append(os.path.join(real_dir, img))

        if os.path.exists(forge_dir):
            for img in os.listdir(forge_dir):
                forge_paths.append(os.path.join(forge_dir, img))

print(f"Found {len(real_paths)} real images, {len(forge_paths)} forged images.")




real_feature = extract_features(real_paths[0])
test_feature = extract_features(forge_paths[0])  # hoặc ảnh upload

cos_sim = cosine_similarity(real_feature, test_feature)[0][0]
euclidean = np.linalg.norm(real_feature - test_feature)

print(f"V Cosine Similarity: {cos_sim:.4f}")
print(f"X Euclidean Distance: {euclidean:.4f}")

if cos_sim > 0.85:
    print("V Kết luận: Chữ ký giống nhau (THẬT)")
else:
    print("X Kết luận: Chữ ký KHÁC nhau (GIẢ)")

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


@auth_bp.route('/verify-signature', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        file = request.files['signature']
        if file:
            filename = secure_filename(file.filename)
            UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'Handwritten_Signature_Verification', 'Dataset')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)

            # Trích đặc trưng ảnh upload
            feature_upload = extract_features(upload_path)

            # So sánh với nhiều mẫu thật
            cos_similarities = []
            euclidean_distances = []

            # Có thể chỉ lấy 5 mẫu thật đầu tiên (để giảm thời gian tính toán)
            num_samples = 5
            for real_path in real_paths[:num_samples]:
                feature_real = extract_features(real_path)
                cos_sim = cosine_similarity(feature_real, feature_upload)[0][0]
                euclidean = np.linalg.norm(feature_real - feature_upload)

                cos_similarities.append(cos_sim)
                euclidean_distances.append(euclidean)

            # Tính giá trị trung bình / tối đa
            avg_cos_sim = np.mean(cos_similarities)
            min_euclidean = np.min(euclidean_distances)

            # Ngưỡng phân biệt tốt hơn (đã giảm nhẹ)
            threshold_cos = 0.70

            if avg_cos_sim > threshold_cos:
                result = "V Chữ ký giống nhau (THẬT)"
            else:
                result = "X Chữ ký khác nhau (GIẢ)"

            return render_template('verify_signature.html',
                                   result=result,
                                   cos_sim=f"{avg_cos_sim:.4f}",
                                   euclidean=f"{min_euclidean:.4f}")
    return render_template('verify_signature.html')
