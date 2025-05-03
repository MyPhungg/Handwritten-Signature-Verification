from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import SmallInteger
from datetime import datetime
db = SQLAlchemy()
# Model accountkh


class AccountKH(db.Model):
    __tablename__ = 'accountkh'

    IdLogin = db.Column(db.String(10), primary_key=True)
    TenDangNhap = db.Column(db.String(50), nullable=False)
    MatKhau = db.Column(db.String(50), nullable=False)
    MaKH = db.Column(db.String(10), db.ForeignKey(
        'khachhang.MaKH'), nullable=False)

    khachhang = db.relationship('KhachHang', backref='accountkh')

# Model accountnv


class AccountNV(db.Model):
    __tablename__ = 'accountnv'

    IdLogin = db.Column(db.String(10), primary_key=True)
    TenDangNhap = db.Column(db.String(50), nullable=False)
    MatKhau = db.Column(db.String(50), nullable=False)
    MaNV = db.Column(db.String(10), db.ForeignKey(
        'nhanvien.MaNV'), nullable=False)

    nhanvien = db.relationship('NhanVien', backref='accountnv')

# Model capbackh


class CapBacKH(db.Model):
    __tablename__ = 'capbackh'

    MaCapBac = db.Column(db.String(10), primary_key=True)
    NgayTao = db.Column(db.Date, nullable=False)
    MucDatDuoc = db.Column(db.Integer, nullable=False)
    TenCapBac = db.Column(db.String(50), nullable=False)


# Model chitietkhuyenmai
class ChiTietKhuyenMai(db.Model):
    __tablename__ = 'chitietkhuyenmai'

    MaKM = db.Column(db.String(10), db.ForeignKey(
        'khuyenmai.MaKM'), primary_key=True)
    MaCapBac = db.Column(db.String(10), db.ForeignKey(
        'capbackh.MaCapBac'), primary_key=True)

# Model khachhang


class KhachHang(db.Model):
    __tablename__ = 'khachhang'

    MaKH = db.Column(db.String(10), primary_key=True)
    HoTen = db.Column(db.String(50), nullable=False)
    NgaySinh = db.Column(db.Date, nullable=False)
    SoCCCD = db.Column(db.String(12), nullable=False)
    NgayCapCCCD = db.Column(db.Date, nullable=False)
    NoiCapCCCD = db.Column(db.String(100), nullable=False)
    CoGiaTriDen = db.Column(db.Date, nullable=False)
    QuocTich = db.Column(db.String(50), nullable=False)
    DanToc = db.Column(db.String(50), nullable=False)
    NoiCuTru = db.Column(db.String(100), nullable=False)
    DiaChiHienTai = db.Column(db.String(100), nullable=False)
    DiaChiThuongTru = db.Column(db.String(100), nullable=False)
    GioiTinh = db.Column(db.String(10), nullable=False)
    SoDienThoai = db.Column(db.String(10), nullable=False)
    NgheNghiep = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    MaNVQL = db.Column(db.String(10), db.ForeignKey(
        'nhanvien.MaNV'), nullable=False, default="NV1")
    MaCapBac = db.Column(db.String(10), db.ForeignKey(
        'capbackh.MaCapBac'), nullable=False, default="Thường")
    ChuKy = db.Column(db.String(1000), nullable=False)

    nhanvien = db.relationship('NhanVien', backref='khachhang')
    capbac = db.relationship('CapBacKH', backref='khachhang')

# Model khuyenmai


class KhuyenMai(db.Model):
    __tablename__ = 'khuyenmai'

    MaKM = db.Column(db.String(10), primary_key=True)
    NoiDung = db.Column(db.Text, nullable=False)
    ThoiGian = db.Column(db.Date, nullable=False)
    LoaiTKApDung = db.Column(db.String(10), db.ForeignKey(
        'loaitk.MaLoai'), nullable=False)
    CapBacThanhVien = db.Column(db.String(10), db.ForeignKey(
        'capbackh.MaCapBac'), nullable=True)
    LoaiKM = db.Column(db.String(50), nullable=False)
    GiaTriKM = db.Column(db.Integer, nullable=False)

    loaitk = db.relationship('LoaiTK', backref='khuyenmai')
    capbackh = db.relationship('CapBacKH', backref='khuyenmai')

# Model lichsugiaodich


class LichSuGiaoDich(db.Model):
    __tablename__ = 'lichsugiaodich'

    MaGD = db.Column(db.String(10), primary_key=True)
    NgayGD = db.Column(db.Date, nullable=False)
    ChieuGD = db.Column(db.Integer, nullable=False)
    NoiDungGD = db.Column(db.String(100), nullable=False)
    GiaTriGD = db.Column(db.Integer, nullable=False)
    HinhThuc = db.Column(db.String(100), nullable=False)
    TKGD = db.Column(db.String(50), db.ForeignKey(
        'taikhoan.MaTK'), nullable=False)
    taikhoan = db.relationship('TaiKhoan', backref='lichsugiaodich')

# Model lstichdiem


class LichSuTichDiem(db.Model):
    __tablename__ = 'lichsutichdiem'

    MaADB = db.Column(db.String(10), primary_key=True)
    ThoiGian = db.Column(db.Date, nullable=False)
    Diem = db.Column(db.Integer, nullable=False)
    MaKH = db.Column(db.String(10), db.ForeignKey(
        'khachhang.MaKH'), nullable=False)

    khachhang = db.relationship('KhachHang', backref='lichsutichdiem')

# Model loaitk


class LoaiTK(db.Model):
    __tablename__ = 'loaitk'

    MaLoai = db.Column(db.String(10), primary_key=True)
    TenLoai = db.Column(db.String(100), nullable=False)

# Model nhanvien


class NhanVien(db.Model):
    __tablename__ = 'nhanvien'

    MaNV = db.Column(db.String(10), primary_key=True)
    HoTen = db.Column(db.String(50), nullable=False)
    MaNVQL = db.Column(db.String(10), db.ForeignKey(
        'nhanvien.MaNV'), nullable=False)
    SoCCCD = db.Column(db.String(12), nullable=False)
    SoDienThoai = db.Column(db.String(10), nullable=False)
    isDelete = db.Column(SmallInteger, nullable=False, default=0)

    quanly = db.relationship('NhanVien', remote_side=[
        MaNV], backref='nhanvien')

# Model quanlycapbac


class QuanLyCapBac(db.Model):
    __tablename__ = 'quanlycapbac'

    MaCapBac = db.Column(db.String(10), db.ForeignKey(
        'capbackh.MaCapBac'), primary_key=True)
    MaNV = db.Column(db.String(10), db.ForeignKey(
        'nhanvien.MaNV'), primary_key=True)

# Model taikhoan


class TaiKhoan(db.Model):
    __tablename__ = 'taikhoan'

    MaTK = db.Column(db.String(10), primary_key=True)
    LoaiTK = db.Column(db.String(10), db.ForeignKey(
        'loaitk.MaLoai'), nullable=False)
    SoDu = db.Column(db.Integer, nullable=False)
    MaKH = db.Column(db.String(10), db.ForeignKey(
        'khachhang.MaKH'), nullable=False)
    STK = db.Column(db.String(50), nullable=False)
    NgayDangKy = db.Column(db.Date, nullable=False)
    TrangThai = db.Column(db.Integer, nullable=False)
    # Thời gian đóng tài khoản
    ThoiGianDong = db.Column(db.DateTime, nullable=True)

    loaitk = db.relationship('LoaiTK', backref='taikhoan')
    khachhang = db.relationship('KhachHang', backref='taikhoan')


class SignatureVector(db.Model):
    __tablename__ = 'signature_vectors'

    MaVector = db.Column(db.Integer, primary_key=True)
    MaKH = db.Column(db.String(10), db.ForeignKey('khachhang.MaKH'), nullable=False)
    vector = db.Column(db.Text, nullable=False)  # lưu JSON string
    NgayTao = db.Column(db.DateTime, default=datetime.utcnow)

    khachhang = db.relationship('KhachHang', backref='signature_vectors')


class SavingsSoTietKiem(db.Model):
    __tablename__ = 'savingssotietkiem'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaTK = db.Column(db.String(10),db.ForeignKey('taikhoan.MaTK'), nullable=False)
    SoTienGui = db.Column(db.Integer, nullable=False)
    MaKyHan = db.Column(db.String(10),db.ForeignKey('kyhan.MaKyHan'), nullable=False)
    NgayMo = db.Column(db.Date, nullable=False)
    NgayKetThuc = db.Column(db.Date, nullable=False)
    MaTKNguon = db.Column(db.String(10),db.ForeignKey('taikhoan.MaTK'), nullable=False)

    taikhoannguon = db.relationship('TaiKhoan', backref='taikhoannguontietkiem',foreign_keys=[MaTKNguon])
    taikhoan = db.relationship('TaiKhoan', backref='savingssotietkiem',foreign_keys=[MaTKNguon])
    kyhan = db.relationship('KyHan', backref='savingssotietkiem')

class KyHan(db.Model):
    __tablename__ = 'kyhan'

    MaKyHan = db.Column(db.String(10), primary_key=True)
    KyHan = db.Column(db.Integer, nullable=False)       # đơn vị: tháng
    LaiSuat = db.Column(db.Float, nullable=False)       # đơn vị: phần trăm
