from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model accountKH


class accountKH(db.Model):
    __tablename__ = 'accountKH'
    IdLogin = db.Column(db.String(10), primary_key=True)
    TenDangNhap = db.Column(db.String(50), nullable=False)
    MatKhau = db.Column(db.String(50), nullable=False)
    MaKH = db.Column(db.String(10), nullable=False)

# Model taiKhoan


class taiKhoan(db.Model):
    __tablename__ = 'taikhoan'
    MaTK = db.Column(db.String(10), primary_key=True)
    SoDu = db.Column(db.Integer, nullable=False)
    LoaiTK = db.Column(db.String(10), nullable=False)
    STK = db.Column(db.String(50), nullable=False)
    NgayDangKy = db.Column(db.Date, nullable=False)
    MaKH = db.Column(db.String(10), nullable=False)
