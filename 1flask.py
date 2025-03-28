import numpy as np
import cv2
from datetime import datetime, date
from decimal import Decimal


class NhanVien:
    def __init__(self, MaNV: str, Ho: str, Ten: str):
        self.MaNV = MaNV
        self.Ho = Ho
        self.Ten = Ten


class AccountNV:
    def __init__(self, MaTK: str, MatKhau: str, TenDangNhap: str, IDLogin: str):
        self.MaTK = MaTK
        self.MatKhau = MatKhau
        self.TenDangNhap = TenDangNhap
        self.IDLogin = IDLogin


class KhachHang:
    def __init__(self, CCCD: str, HoTen: str, DiaChi: str,  ChuKy: str, Email: str, NgaySinh: str, NgayCapCCCD: str, NgayHetHanCCCD: str, MaNVQL: str):
        self.CCCD = CCCD
        self.HoTen = HoTen
        self.DiaChi = DiaChi
        self.ChuKy = ChuKy  # duong dan hinh anh
        self.Email = Email
        try:
            ngaycap = datetime.strptime(NgayCapCCCD, "%Y-%m-%d").date()
            today = date.today()
            if NgaySinh > today:
                raise ValueError(
                    "Lỗi: Ngày cấp CCCD không được vượt quá hiện tại.")
            self.NgayCapCCCD = ngaycap
        except ValueError:
            raise ValueError(
                "Ngày cấp CCCD không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")

        self.NgayHetHanCCCD = NgayHetHanCCCD
        try:
            self.NgayHetHanCCCD = datetime.strptime(
                NgayHetHanCCCD, "%Y-%m-%d").date()
            if NgayHetHanCCCD < NgayCapCCCD:
                raise ValueError("Lỗi! Ngày hết hạn CCCD không phù hợp.")
        except ValueError:
            raise ValueError(
                "Lỗi nhập ngày không đúng đinh định dạng YYYY-MM-DD.")
        try:
            ngay_sinh = datetime.strptime(NgaySinh, "%Y-%m-%d").date()
            today = date.today()
            if NgaySinh > today:
                raise ValueError(
                    "Lỗi: Ngày sinh không được vượt quá hiện tại.")
            self.NgaySinh = ngay_sinh
        except ValueError:
            raise ValueError(
                "Ngày sinh không hop lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")


class AccountKH:
    def __init__(self, MatKhau: str, TenDangNhap: str, IDLogin: str):
        self.MatKhau = MatKhau
        self.TenDangNhap = TenDangNhap
        self.IDLogin = IDLogin


class TaiKhoan:
    def __init__(self, MaTK: str, LoaiTK: str, SoDu: str):
        self.MaTK = MaTK
        self.LoaiTK = LoaiTK
        # Decimal quan ly chinh xac so tien hon float
        self.SoDu = Decimal(SoDu)


class LoaiTK:
    def __init__(self, MaLoai: str, TenLoai: str):
        self.Maloai = MaLoai
        self.TenLoai = TenLoai


class LichSuGiaoDich:
    def __init__(self, MaGD: str, NgayGD: str, NguoiGD: str, ChieuGD: str, NDGD: str, GiaTriGD: str, HinhThuc: str):
        self.MaDG = MaGD
        self.NguoiGD = NguoiGD
        self.ChieuGD = ChieuGD
        self.NDGD = NDGD
        self.GiaTriGD = Decimal(GiaTriGD)
        self.HinhThuc = HinhThuc
        try:
            ngaygd = datetime.strptime(NgayGD, "%Y-%m-%d").date()
            today = date.today()
            if ngaygd > today:
                raise ValueError("Ngày giao dịch không được vuọt quá hôm nay.")
            self.NgayGD = ngaygd
        except ValueError:
            raise ValueError("Vui lòng nhập đúng định dạng YYYY-MM-DD.")


class CapBacKhachHang:
    def __init__(self, MaCapBac: str, NgayTao: str, MucDatDuoc: str, TenCapBac: str, MaNVQL: str):
        self.MaCapBac = MaCapBac
        self.MacDatDuoc = Decimal(MucDatDuoc)
        self.TenCapBac = TenCapBac
        self.MaNVQL = MaNVQL
        try:
            ngaytao = datetime.strptime(NgayTao, "%Y-%m-%d").date()
            today = date.today()
            if ngaytao > today:
                raise ValueError("Ngày tạo không được vượt quá hôm nay.")
            self.NgayTao = ngaytao
        except ValueError:
            raise ValueError("Lỗi! Ngay tạo không đúng định dạng YYYY-MM-DD.")


class KhuyenMai:
    def __init__(self, MaKM: str, LoaiKM: str, NoiDung: str, NgayBD: str, NgayKT: str, LoaiTKApDung: str):
        self.MaKM = MaKM
        self.LoaiKM = LoaiKM
        self.NoiDung = NoiDung
        self.LoaiTKApDung = LoaiTKApDung.split()  # dinh dang chuoi a,b,c
        try:
            self.NgayBD = datetime.strptime(NgayBD, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Lỗi nhập không đúng định dạng YYYY-MM-DD.")
        try:
            self.NgayKT = datetime.strptime(NgayBD, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Lỗi nhập không đúng định dạng YYYY-MM-DD.")


class ChiTietKhuyenMai:
    def __init__(self, MaCapBac: str, MaKM: str):
        self.MaCapBac = MaCapBac
        self.MaKM = MaKM


class QuanLyNhanVien:


class QuanLyKhachHang:


class QuanLyCapBacThe:


class QuanLyTaiKhoan:
