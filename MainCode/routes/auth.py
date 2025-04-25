from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import AccountKH, KhachHang, AccountNV, NhanVien, SignatureVector, TaiKhoan
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import model_from_json, Model
from datetime import datetime
import numpy as np
import os
import cv2
import json
from models import db
# Blueprint
auth_bp = Blueprint('auth', __name__)

# Load mô hình
base_model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Handwritten_Signature_Verification')
with open(os.path.join(base_model_path, "model.json"), "r") as json_file:
    model = model_from_json(json_file.read())
model.load_weights(os.path.join(base_model_path, "model.weights.h5"))

# Trích xuất đặc trưng từ lớp áp chót
intermediate_layer_model = Model(inputs=model.input, outputs=model.layers[-2].output)

# Hàm xoay ảnh
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Hàm trích đặc trưng có xoay ảnh
def extract_augmented_features(image_path, angles=None):
    if angles is None:
        angles = [-15, -12, -9, -6, -3, 0, 3, 6, 9, 12]

    image = cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    feature_list = []

    for angle in angles:
        rotated_img = rotate_image(image, angle)
        rotated_img = rotated_img.astype('float32') / 255.0
        rotated_img = np.expand_dims(rotated_img, axis=0)
        feature = intermediate_layer_model.predict(rotated_img)[0]
        feature_list.append(feature)

    mean_feature = np.mean(feature_list, axis=0)
    return mean_feature

# Lưu vector chữ ký vào DB (ảnh đã xoay và lấy trung bình)
def save_mean_signature_vector(folder_path,ma_kh):
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại.")
        return

    image_paths = [os.path.join(folder_path, fname)
                   for fname in os.listdir(folder_path)
                   if fname.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if len(image_paths) == 0:
        print(f"Không tìm thấy ảnh chữ ký trong {folder_path}")
        return
    
    vectors = [extract_augmented_features(img_path) for img_path in image_paths]
    mean_vector = np.mean(vectors, axis=0)

    # Tạo giá trị mới cho MaVector bằng cách truy vấn giá trị lớn nhất trong database
    last_vector = db.session.query(db.func.max(SignatureVector.MaVector)).scalar()

    if last_vector:
        # Kiểm tra nếu last_vector là chuỗi, cắt chuỗi và tăng giá trị, nếu là int thì tăng trực tiếp
        if isinstance(last_vector, str):
            last_vector_number = int(last_vector[2:])  # Cắt chuỗi và lấy phần số
            new_ma_vector = f"MV{last_vector_number + 1:03d}"  # Tạo MaVector mới
        elif isinstance(last_vector, int):
            new_ma_vector = f"MV{last_vector + 1:03d}"  # Tăng trực tiếp nếu last_vector là số nguyên
    else:
        # Nếu chưa có bản ghi nào, bắt đầu từ 'MV001'
        new_ma_vector = "MV001"

    new_vector = SignatureVector(
        MaVector=new_ma_vector,  # Sử dụng giá trị mới cho MaVector
        MaKH=ma_kh,
        vector=json.dumps(mean_vector.tolist()),
        NgayTao=datetime.now()
    )
    db.session.add(new_vector)
    db.session.commit()


# Lấy vector từ DB
def get_vector_from_db(ma_kh):
    entry = SignatureVector.query.filter_by(MaKH=ma_kh).order_by(SignatureVector.NgayTao.desc()).first()
    if entry:
        vector_list = json.loads(entry.vector)
        return np.array(vector_list)
    return None

# Xác thực chữ ký dựa trên cosine + euclidean
def compare_vectors(feature1, feature2, threshold=0.85):
    cos_sim = cosine_similarity([feature1], [feature2])[0][0]
    euclidean = np.linalg.norm(feature1 - feature2)
    result = True if cos_sim > threshold else False
    return {
        "result": result,
        "cosine_similarity": round(float(cos_sim), 4),
        "euclidean_distance": round(float(euclidean), 4)
    }


# Hàm xác thực chữ ký (ảnh test được xoay và trích trung bình đặc trưng)

def verify_signature_with_augmentation(file, ma_kh, threshold=0.85):
    """
    Xác thực chữ ký bằng cách xoay ảnh, trích xuất đặc trưng trung bình và so sánh với vector từ DB.
    Trả về True nếu khớp, False nếu không.
    """
    try:
        # Bước 1: Đọc ảnh từ bộ nhớ
        in_memory_file = file.read()
        nparr = np.frombuffer(in_memory_file, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return {
                "result": False,
                "message": "Không thể đọc ảnh từ file upload."
            }

        # Bước 2: Trích đặc trưng từ ảnh đã xử lý augmentation
        test_vector = extract_augmented_features(image)

        # Bước 3: Lấy vector mẫu từ DB
        reference_vector = get_vector_from_db(ma_kh)
        if reference_vector is None:
            return {
                "result": False,
                "message": "Không tìm thấy vector mẫu trong cơ sở dữ liệu."
            }

        # Bước 4: So sánh vector
        return compare_vectors(test_vector, reference_vector, threshold)

    except Exception as e:
        return {
            "result": False,
            "message": f"Lỗi trong quá trình xác thực: {str(e)}"
        }




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

def process_forgot_account(soDienThoai, authMethod, cccd=None, file=None):
    # Tìm người dùng theo số điện thoại (ưu tiên Khách Hàng trước)
    user = KhachHang.query.filter_by(SoDienThoai=soDienThoai).first()
    if not user:
        user = NhanVien.query.filter_by(SoDienThoai=soDienThoai).first()
    if not user:
        flash('Không tồn tại tài khoản liên kết với số điện thoại này!', 'error')
        return render_template('forgetAcc.html', soDienThoai=soDienThoai)

    # ==== XÁC THỰC CCCD ====
    if authMethod == 'cccd':
        if user.SoCCCD != cccd:
            flash('Số CCCD không khớp!', 'error')
            return render_template('forgetAcc.html', soDienThoai=soDienThoai, cccd=cccd)

        if isinstance(user, KhachHang):
            account = AccountKH.query.filter_by(MaKH=user.MaKH).first()
        else:  # Nhân viên
            account = AccountNV.query.filter_by(MaNV=user.MaNV).first()

        if not account:
            flash('Lỗi trong việc tìm kiếm tài khoản', 'error')
            return render_template('forgetAcc.html', soDienThoai=soDienThoai, cccd=cccd)

        flash('Xác thực CCCD thành công!')
        return render_template('forgetAcc.html',
                               soDienThoai=soDienThoai,
                               username=account.TenDangNhap,
                               show_result=True)

    # ==== XÁC THỰC CHỮ KÝ ====
    elif authMethod == 'signature':
        if not file or file.filename == '':
            flash("Chưa chọn ảnh chữ ký!", "danger")
            return render_template('forgetAcc.html', soDienThoai=soDienThoai)

        if not isinstance(user, KhachHang):
            flash("Chỉ hỗ trợ xác thực chữ ký cho khách hàng!", "danger")
            return render_template('forgetAcc.html', soDienThoai=soDienThoai)

        account = AccountKH.query.filter_by(MaKH=user.MaKH).first()
        if not account:
            flash('Không tìm thấy tài khoản khách hàng!', 'error')
            return render_template('forgetAcc.html', soDienThoai=soDienThoai)

        result_verify = verify_signature_with_augmentation(file,user.MaKH)

            
        if result_verify['result']:
            flash('Xác thực chữ ký thành công!')
            return render_template('forgetAcc.html',
                                   soDienThoai=soDienThoai,
                                   username=account.TenDangNhap,
                                   show_result=True)
        else:
            flash('Chữ ký không trùng khớp!', 'error')
    else:
        flash('Không tìm thấy chữ ký gốc trong hệ thống!', 'error')

        return render_template('forgetAcc.html', soDienThoai=soDienThoai)

@auth_bp.route('/login/forgetAcc/submit', methods=['GET', 'POST'])
def forgetAccSubmit():
    if request.method == 'POST':
        soDienThoai = request.form.get('soDienThoai')
        authMethod = request.form.get('authMethod')

        if authMethod == 'cccd':
            cccd = request.form.get('cccd')
            return process_forgot_account(soDienThoai, authMethod, cccd=cccd)
        elif authMethod == 'signature':
            file = request.files.get('signature')
            return process_forgot_account(soDienThoai, authMethod, file=file)

    flash('Vui lòng chọn phương thức xác nhận', 'error')
    return redirect(url_for('auth.forgetAcc'))


# Chuyển hướng tới trang quên mật khẩu

@auth_bp.route('/login/forgetPass', methods=['GET'])
def forgetPass():
    return render_template('forgetPass.html')

# Xử lý quên mật khẩu

@auth_bp.route('/verify-signature', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        file = request.files['signature']
        username_input = request.form.get('username')

        if file and username_input:
            # Dùng SQLAlchemy để truy vấn username
            account = AccountKH.query.filter_by(TenDangNhap=username_input).first()

            if account:
                ma_kh = account.MaKH
                username = account.TenDangNhap
                password = account.MatKhau

                result_verify = verify_signature_with_augmentation(file,ma_kh)
                if result_verify['result']:
                    result = "Xác thực thành công"
                    cos_sim = result['cosine_similarity']
                    euclidean = result['euclidean_distance']
                else:
                    result = "Chữ ký không trùng khớp"
                    username = password = ""
                    cos_sim = euclidean = None
            else:
                result = "Không tìm thấy chữ ký gốc"
                username = password = ""
                cos_sim = euclidean = None

        else:
            result = "Không tìm thấy tài khoản"
            username = password = ""
            cos_sim = euclidean = None

        return render_template('forgetPass.html',
                               result=result,
                               username=username,
                               password=password,
                               cos_sim=f"{cos_sim}" if cos_sim else "N/A",
                               euclidean=f"{euclidean}" if euclidean else "N/A",
                               show_result=True)

    return render_template('forgetPass.html', show_result=False)

# Xác thực CCCD - cả Khách hàng và Nhân viên
@auth_bp.route('/verify-cccd', methods=['POST'])
def verify_cccd():
    username_input = request.form.get('username')
    cccd_input = request.form.get('cccd')

    if username_input and cccd_input:
        # -------- Kiểm tra trong tài khoản khách hàng --------
        account_kh = AccountKH.query.filter_by(TenDangNhap=username_input).first()
        if account_kh:
            khachhang = KhachHang.query.filter_by(MaKH=account_kh.MaKH, SoCCCD=cccd_input).first()
            if khachhang:
                return render_template('forgetPass.html',
                                       result="Xác thực thành công (Khách hàng)",
                                       username=account_kh.TenDangNhap,
                                       password=account_kh.MatKhau,
                                       cos_sim="N/A",
                                       euclidean="N/A",
                                       show_result=True)

        # -------- Kiểm tra trong tài khoản nhân viên --------
        account_nv = AccountNV.query.filter_by(TenDangNhap=username_input).first()
        if account_nv:
            nhanvien = NhanVien.query.filter_by(MaNV=account_nv.MaNV, SoCCCD=cccd_input).first()
            if nhanvien:
                return render_template('forgetPass.html',
                                       result="Xác thực thành công (Nhân viên)",
                                       username=account_nv.TenDangNhap,
                                       password=account_nv.MatKhau,
                                       cos_sim="N/A",
                                       euclidean="N/A",
                                       show_result=True)

        # Không tìm thấy ở cả hai
        return render_template('forgetPass.html',
                               result="Sai tên đăng nhập hoặc CCCD",
                               username="",
                               password="",
                               cos_sim="N/A",
                               euclidean="N/A",
                               show_result=True)

    # Nếu thiếu thông tin
    return render_template('forgetPass.html', show_result=False)

# Nhan viên xác thực chữ ký khi thao tác thông tin khách hàng (xóa,sửa)

@auth_bp.route('/verify-signature-change', methods=['POST'])
def verify_signature_to_change_kh():
    maKH = request.form.get('maKH')
    come = request.form.get('come')  # template khi xác thực thành công
    back = request.form.get('back')  # template khi thất bại
    file = request.files['signature']
    kh = KhachHang.query.filter_by(MaKH=maKH).first()


    if not kh:
        flash('Không tìm thấy khách hàng!', 'error')
        return redirect(url_for(back, maKH=kh.MaKH))

    if not file:
        flash('Vui lòng tải lên chữ ký!', 'error')
        return redirect(url_for(back, maKH=kh.MaKH))

    result_verify = verify_signature_with_augmentation(file,maKH)
    if result_verify['result']:
        flash('Xác thực thành công!', 'success')
        return redirect(url_for(come, maKH=kh.MaKH))

    flash('Chữ ký không trùng khớp!', 'error')
    return redirect(url_for(back, maKH=kh.MaKH))

@auth_bp.route('/change_status', methods=['POST'])
def dong_mo_tai_khoan():
    maKH = request.form.get('maKH')
    maTK = request.form.get('maTK')
    file = request.files.get('signature')

    kh = KhachHang.query.filter_by(MaKH=maKH).first()
    taikhoan = TaiKhoan.query.filter_by(MaTK=maTK).first()

    if not kh or not taikhoan:
        flash('Không tìm thấy khách hàng hoặc tài khoản.', 'danger')
        return redirect(url_for('home.admin_khachhang', khach_hang=kh))

    if not file:
        flash('Vui lòng tải lên ảnh chữ ký!', 'warning')
        return redirect(url_for('home.admin_khachhang', khach_hang=kh))

    result_verify = verify_signature_with_augmentation(file, maKH)

    if result_verify['result']:
        if taikhoan.TrangThai == 1:
            taikhoan.TrangThai = 0
            flash('Đã **đóng tài khoản** thành công.', 'success')
        else:
            taikhoan.TrangThai = 1
            flash('Tài khoản đã được **mở lại**.', 'success')

        db.session.commit()
        return redirect(url_for('home.admin_khachhang')) 
    else:
        flash('Chữ ký không hợp lệ!', 'error')
        return render_template(
            'admin/chinhsuaKH.html',
            tai_khoan_list=TaiKhoan.query.all(),
            show_modal=maTK
        )





