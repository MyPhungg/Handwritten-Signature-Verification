from flask_sqlalchemy import SQLAlchemy

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
        'nhanvien.MaNV'), nullable=False)
    MaCapBac = db.Column(db.String(10), db.ForeignKey(
        'capbackh.MaCapBac'), nullable=False)
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
    LoaiKM = db.Column(db.String(50), nullable=False)
    GiaTriKM = db.Column(db.Integer, nullable=False)

    loaitk = db.relationship('LoaiTK', backref='khuyenmai')

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

    loaitk = db.relationship('LoaiTK', backref='taikhoan')
    khachhang = db.relationship('KhachHang', backref='taikhoan')
