# from flask import Flask, render_template, request
# from flask import redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/bank"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "hiden"  # khóa bí mật để mã hóa session
# db = SQLAlchemy(app)


# # Tạo bảng trong CSDL (chỉ cần chạy một lần)
# with app.app_context():
#     db.create_all()

# # Route cho trang đăng nhập


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     print(request.form)  # In dữ liệu form ra terminal để kiểm tra
#     if request.method == 'POST':
#         username = request.form.get('username')  # lấy name chứ không lấy id
#         password = request.form.get('password')

#         # Kiểm tra thông tin đăng nhập
#         account = accountKH.query.filter_by(
#             TenDangNhap=username, MatKhau=password).first()
#         if account:
#             # Lưu IdLogin vào session
#             session['MaKH'] = account.MaKH
#             # Chuyển đến trang chooseAcc.html
#             return redirect(url_for('chooseAcc'))
#         else:
#             flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
#     return render_template('login.html')


# # Route cho trang chọn tài khoản

# @app.route('/login/chooseAcc', methods=['GET', 'POST'])
# def chooseAcc():
#     if 'MaKH' not in session:
#         flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         selected_MaTK = request.form.get('taikhoan')
#         if selected_MaTK:
#             # Lưu MaTK được chọn vào session
#             session['MaTK'] = selected_MaTK
#             return redirect(url_for('home'))
#         else:
#             flash('Vui lòng chọn một tài khoản!', 'error')

#     # Lấy danh sách tài khoản dựa trên MaKH từ session
#     maKH = session['MaKH']
#     dsTaiKhoan = taiKhoan.query.filter_by(MaKH=maKH).all()
#     return render_template('chooseAcc.html', dsTaiKhoan=dsTaiKhoan)


# # Route cho trang chủ


# @app.route('/home')
# def home():
#     if 'MaTK' not in session:
#         flash('Vvui lòng chọn tài khoản trước!', 'error')
#         return redirect(url_for('chooseAcc'))

#     # Lấy thông tin tài khoản được chọn
#     maTK = session['MaTK']
#     tk = taiKhoan.query.get(maTK)
#     return render_template('home.html', tk=tk)

# # Route để đăng xuất


# @app.route('/logout')
# def logout():
#     # Xóa session
#     session.pop('MaKH', None)
#     session.pop('MaTK', None)
#     flash('Bạn đã đăng xuất!', 'success')
#     return redirect(url_for('login'))


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
