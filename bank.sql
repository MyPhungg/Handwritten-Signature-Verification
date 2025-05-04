-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 04, 2025 lúc 06:46 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `bank`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `accountkh`
--

CREATE TABLE `accountkh` (
  `IdLogin` varchar(10) NOT NULL,
  `TenDangNhap` varchar(50) NOT NULL,
  `MatKhau` varchar(50) NOT NULL,
  `MaKH` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `accountkh`
--

INSERT INTO `accountkh` (`IdLogin`, `TenDangNhap`, `MatKhau`, `MaKH`) VALUES
('CL1', 'skyblue123', 'S@fep@ss01', 'KH1'),
('CL10', 'cosmic_dust', 'St@rG@zer42', 'KH10'),
('CL11', 'desert_fox', 'S@nd&Wind99', 'KH11'),
('CL12', 'mountain_peak', 'Everest@123', 'KH12'),
('CL13', 'frozenlake', 'Ic3Que3n2025', 'KH13'),
('CL14', 'thunderstrike', 'Lightning!Fast9', 'KH14'),
('CL15', 'shadowhunter', 'N1ghtSt@lker77', 'KH15'),
('CL16', 'goldenhour', 'SunsetLover!55', 'KH16'),
('CL17', 'darkknight', 'Batm@nRul3s', 'KH17'),
('CL2', 'ocean_wind', 'Tr@velL0ver!', 'KH2'),
('CL3', 'midnightowl', 'N1ght0wl!23', 'KH3'),
('CL4', 'sunny_day', 'Br1ght&Shiny', 'KH4'),
('CL5', 'storm_rider', 'Thund3rC@t$', 'KH5'),
('CL6', 'greenleaf99', 'Tr33Hugger2024', 'KH6'),
('CL7', 'silentwhisper', 'Shhh@Secret77', 'KH7'),
('CL8', 'redphoenix', 'FireB1rd!Rising', 'KH8'),
('CL9', 'moonlitshadow', 'D@rkMoon88', 'KH9');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `accountnv`
--

CREATE TABLE `accountnv` (
  `IdLogin` varchar(10) NOT NULL,
  `TenDangNhap` varchar(50) NOT NULL,
  `MatKhau` varchar(50) NOT NULL,
  `MaNV` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `accountnv`
--

INSERT INTO `accountnv` (`IdLogin`, `TenDangNhap`, `MatKhau`, `MaNV`) VALUES
('SL1', 'nguyenvana', 'password123', 'NV1'),
('SL10', 'tothij', 'strongpass!', 'NV10'),
('SL2', 'tranthib', 'abc@123', 'NV2'),
('SL3', 'levanc', 'qwerty456', 'NV3'),
('SL4', 'phamthid', 'securepass', 'NV4'),
('SL5', 'hoangvane', 'letmein789', 'NV5'),
('SL6', 'dangthif', 'pass@word1', 'NV6'),
('SL7', 'buivang', '1234abcd', 'NV7'),
('SL8', 'vuthih', 'h@rd2gu3ss', 'NV8'),
('SL9', 'lyvani', 'myp@ssword', 'NV9');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `capbackh`
--

CREATE TABLE `capbackh` (
  `MaCapBac` varchar(10) NOT NULL,
  `NgayTao` date NOT NULL,
  `MucDatDuoc` int(11) NOT NULL,
  `TenCapBac` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `capbackh`
--

INSERT INTO `capbackh` (`MaCapBac`, `NgayTao`, `MucDatDuoc`, `TenCapBac`) VALUES
('BC1021', '2025-03-25', 2147483647, 'Ruby'),
('CB1', '2025-03-20', 0, 'Thường'),
('CB2', '2025-03-20', 20000000, 'Bạc'),
('CB3', '2025-03-20', 100000000, 'Vàng'),
('CB4', '2025-03-20', 500000000, 'Kim Cương');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chitietkhuyenmai`
--

CREATE TABLE `chitietkhuyenmai` (
  `MaKM` varchar(10) NOT NULL,
  `MaCapBac` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `chitietkhuyenmai`
--

INSERT INTO `chitietkhuyenmai` (`MaKM`, `MaCapBac`) VALUES
('KM10', 'CB3'),
('KM2', 'CB2'),
('KM3', 'CB3'),
('KM4', 'CB4'),
('KM5', 'CB1'),
('KM6', 'CB2'),
('KM7', 'CB3'),
('KM8', 'CB4'),
('KM9', 'CB1');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `khachhang`
--

CREATE TABLE `khachhang` (
  `MaKH` varchar(10) NOT NULL,
  `HoTen` varchar(50) NOT NULL,
  `NgaySinh` date NOT NULL,
  `SoCCCD` varchar(12) NOT NULL,
  `NgayCapCCCD` date NOT NULL,
  `NoiCapCCCD` varchar(100) NOT NULL,
  `CoGiaTriDen` date NOT NULL,
  `QuocTich` varchar(50) NOT NULL,
  `DanToc` varchar(50) NOT NULL,
  `NoiCuTru` varchar(100) NOT NULL,
  `DiaChiHienTai` varchar(100) NOT NULL,
  `DiaChiThuongTru` varchar(100) NOT NULL,
  `GioiTinh` varchar(10) NOT NULL,
  `SoDienThoai` varchar(10) NOT NULL,
  `NgheNghiep` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `MaNVQL` varchar(10) NOT NULL,
  `MaCapBac` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `khachhang`
--

INSERT INTO `khachhang` (`MaKH`, `HoTen`, `NgaySinh`, `SoCCCD`, `NgayCapCCCD`, `NoiCapCCCD`, `CoGiaTriDen`, `QuocTich`, `DanToc`, `NoiCuTru`, `DiaChiHienTai`, `DiaChiThuongTru`, `GioiTinh`, `SoDienThoai`, `NgheNghiep`, `Email`, `MaNVQL`, `MaCapBac`) VALUES
('KH1', 'Nguyễn Văn A', '1995-06-16', '023456789012', '2020-01-01', 'Hà Nội', '2030-01-01', 'Việt Nam', 'Kinh', 'Hà Nội', 'Hà Nội', 'Hà Nội', 'Nam', '0123456789', 'Kinh doanh', 'b@gmail.com', 'NV1', 'CB1'),
('KH10', 'Tạ Thị J', '1983-03-19', '999000111222', '2012-12-05', 'Quảng Nam', '2022-12-05', 'Việt Nam', 'Kinh', 'Quảng Nam', 'Quảng Nam', 'Quảng Nam', 'Nữ', '0988889999', 'Giảng viên', 'j@gmail.com', 'NV8', 'CB4'),
('KH11', 'Nguyễn Văn K', '1992-07-14', '112233445566', '2011-07-10', 'Hà Giang', '2021-07-10', 'Việt Nam', 'Kinh', 'Hà Giang', 'Hà Giang', 'Hà Giang', 'Nam', '0999990000', 'Công an', 'k@gmail.com', 'NV1', 'CB1'),
('KH12', 'Trần Thị L', '1999-06-21', '667788990011', '2021-01-10', 'Phú Yên', '2031-01-10', 'Việt Nam', 'Kinh', 'Phú Yên', 'Phú Yên', 'Phú Yên', 'Nữ', '0101010101', 'Dược sĩ', 'l@gmail.com', 'NV2', 'CB1'),
('KH13', 'Hoàng Văn M', '1993-09-30', '223344556677', '2018-11-20', 'Hậu Giang', '2028-11-20', 'Việt Nam', 'Kinh', 'Hậu Giang', 'Hậu Giang', 'Hậu Giang', 'Nam', '0111112222', 'Kinh doanh', 'm@gmail.com', 'NV9', 'CB1'),
('KH14', 'Đinh Thị N', '2001-01-15', '334455667788', '2020-03-25', 'Lào Cai', '2030-03-25', 'Việt Nam', 'Kinh', 'Lào Cai', 'Lào Cai', 'Lào Cai', 'Nữ', '0122223333', 'Sinh viên', 'n@gmail.com', 'NV10', 'CB2'),
('KH15', 'Lê Văn O', '1996-05-12', '445566778899', '2016-06-15', 'Đồng Nai', '2026-06-15', 'Việt Nam', 'Kinh', 'Đồng Nai', 'Đồng Nai', 'Đồng Nai', 'Nam', '0133334444', 'Cơ khí', 'o@gmail.com', 'NV3', 'CB2'),
('KH16', 'Bùi Thị P', '1990-04-09', '556677889900', '2015-08-05', 'Bình Thuận', '2025-08-05', 'Việt Nam', 'Kinh', 'Bình Thuận', 'Bình Thuận', 'Bình Thuận', 'Nữ', '0144445555', 'Y tá', 'p@gmail.com', 'NV4', 'CB2'),
('KH17', 'Phạm Văn Q', '1986-07-17', '667788990011', '2014-09-20', 'Sóc Trăng', '2024-09-20', 'Việt Nam', 'Kinh', 'Sóc Trăng', 'Sóc Trăng', 'Sóc Trăng', 'Nam', '0155556666', 'Công nhân', 'q@gmail.com', 'NV5', 'CB3'),
('KH2', 'Trần Thị B', '1998-07-22', '987654321098', '2019-02-20', 'TP.HCM', '2029-02-20', 'Việt Nam', 'Kinh', 'TP.HCM', 'TP.HCM', 'TP.HCM', 'Nữ', '0987654321', 'Nhân viên văn phòng', 'b@gmail.com', 'NV2', 'CB1'),
('KH3', 'Lê Văn C', '1990-09-10', '123123123123', '2018-03-10', 'Đà Nẵng', '2028-03-10', 'Việt Nam', 'Kinh', 'Đà Nẵng', 'Đà Nẵng', 'Đà Nẵng', 'Nam', '0909090909', 'Kỹ sư', 'c@gmail.com', 'NV9', 'CB1'),
('KH4', '', '1985-05-05', '321321321321', '2017-04-15', 'Cần Thơ', '2027-04-15', 'Việt Nam', 'Kinh', 'Cần Thơ', 'Cần Thơ', 'Cần Thơ', 'Nữ', '0912121212', 'Giáo viên', 'd@gmail.com', 'NV10', 'CB2'),
('KH5', 'Hoàng Văn E', '2000-12-30', '111222333444', '2021-06-25', 'Hải Phòng', '2031-06-25', 'Việt Nam', 'Kinh', 'Hải Phòng', 'Hải Phòng', 'Hải Phòng', 'Nam', '0933334444', 'Sinh viên', 'e@gmail.com', 'NV3', 'CB2'),
('KH6', 'Ngô Thị F', '1997-04-18', '444333222111', '2016-07-10', 'Nghệ An', '2026-07-10', 'Việt Nam', 'Kinh', 'Nghệ An', 'Nghệ An', 'Nghệ An', 'Nữ', '0944445555', 'Bác sĩ', 'f@gmail.com', 'NV4', 'CB2'),
('KH7', 'Đặng Văn G', '1994-11-09', '555666777888', '2015-05-20', 'Huế', '2025-05-20', 'Việt Nam', 'Kinh', 'Huế', 'Huế', 'Huế', 'Nam', '0955556666', 'Nhân viên IT', 'g@gmail.com', 'NV5', 'CB3'),
('KH8', 'Lý Thị H', '1991-08-07', '777888999000', '2014-08-30', 'Bắc Ninh', '2024-08-30', 'Việt Nam', 'Kinh', 'Bắc Ninh', 'Bắc Ninh', 'Bắc Ninh', 'Nữ', '0966667777', 'Luật sư', 'h@gmail.com', 'NV6', 'CB3'),
('KH9', 'Vũ Văn I', '1988-10-25', '888999000111', '2013-09-25', 'Thanh Hóa', '2023-09-25', 'Việt Nam', 'Kinh', 'Thanh Hóa', 'Thanh Hóa', 'Thanh Hóa', 'Nam', '0977778888', 'Kiến trúc sư', 'i@gmail.com', 'NV7', 'CB4');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `khuyenmai`
--

CREATE TABLE `khuyenmai` (
  `MaKM` varchar(10) NOT NULL,
  `NoiDung` text NOT NULL,
  `ThoiGian` date NOT NULL,
  `LoaiTKApDung` varchar(10) NOT NULL,
  `LoaiKM` varchar(50) NOT NULL,
  `GiaTriKM` int(11) NOT NULL,
  `CapBacThanhVien` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `khuyenmai`
--

INSERT INTO `khuyenmai` (`MaKM`, `NoiDung`, `ThoiGian`, `LoaiTKApDung`, `LoaiKM`, `GiaTriKM`, `CapBacThanhVien`) VALUES
('KM10', 'Giảm lãi suất vay cho khách hàng lâu năm (Tín dụng)', '2025-05-15', 'ML1', 'Giảm', 3, 'CB2'),
('KM123', 'Ưu đãi 10%', '2025-04-01', 'ML2', 'Giảm giá', 10, NULL),
('KM2', 'Giảm lãi suất vay cho tài khoản Tín dụng', '2025-04-05', 'ML1', 'Giảm', 2, 'CB1'),
('KM3', 'Tăng lãi suất khi gửi trên 500 triệu với tài khoản Tiết kiệm', '2025-04-10', 'ML2', 'Tăng', 1, 'CB4'),
('KM321', 'Ưu đãi VIP', '2025-04-01', 'ML1', 'Tặng quà', 50, 'CB1'),
('KM4', 'Giảm phí rút tiền trước hạn cho tài khoản Tiết kiệm', '2025-04-15', 'ML2', 'Giảm', 2, NULL),
('KM5', 'Tăng lãi suất cho tài khoản Tiết kiệm từ 1 tỷ', '2025-04-20', 'ML2', 'Tăng', 2, NULL),
('KM6', 'Giảm lãi suất vay cho tài khoản Ghi nợ', '2025-04-25', 'ML3', 'Giảm', 1, NULL),
('KM7', 'Tăng lãi suất khi gửi từ 2 tỷ với tài khoản Tiết kiệm', '2025-04-30', 'ML2', 'Tăng', 3, 'CB1'),
('KM8', 'Giảm phí duy trì tài khoản Tín dụng', '2025-05-05', 'ML1', 'Giảm', 1, NULL),
('KM9', 'Tăng lãi suất khi tái gửi với tài khoản Tiết kiệm', '2025-05-10', 'ML2', 'Tăng', 2, NULL),
('UD1201', 'test TK1 TK tiet kiem', '2025-03-30', 'ML1', 'Giảm', 1, 'CB1');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `kyhan`
--

CREATE TABLE `kyhan` (
  `MaKyHan` varchar(10) NOT NULL,
  `KyHan` int(11) NOT NULL,
  `LaiSuat` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `kyhan`
--

INSERT INTO `kyhan` (`MaKyHan`, `KyHan`, `LaiSuat`) VALUES
('H1', 1, 1.7),
('H2', 3, 2),
('H3', 6, 3),
('H4', 12, 4.7);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lichsugiaodich`
--

CREATE TABLE `lichsugiaodich` (
  `MaGD` varchar(10) NOT NULL,
  `NgayGD` date NOT NULL,
  `ChieuGD` int(11) NOT NULL,
  `NoiDungGD` varchar(100) NOT NULL,
  `GiaTriGD` int(11) NOT NULL,
  `HinhThuc` varchar(100) NOT NULL,
  `TKGD` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `lichsugiaodich`
--

INSERT INTO `lichsugiaodich` (`MaGD`, `NgayGD`, `ChieuGD`, `NoiDungGD`, `GiaTriGD`, `HinhThuc`, `TKGD`) VALUES
('GD2', '2025-04-03', 0, 'a', 11000000, 'Gửi tiết kiệm', 'TK24'),
('GD302', '2025-05-03', 1, 'Tất toán sổ tiết kiệm', 101700, 'Tất toán sổ tiết kiệm', 'TK1'),
('GD303', '2025-05-04', 1, 'Nạp tiền', 10000000, 'Nạp tiền', 'TK26'),
('GD304', '2025-05-04', 0, 'Tất toán sổ tiết kiệm', 1000000, 'mo so tiet kiem', 'TK24'),
('GD305', '2025-05-04', 1, 'Tất toán sổ tiết kiệm', 1017000, 'Tất toán sổ tiết kiệm', 'TK24'),
('GD306', '2025-05-04', 0, 'Gửi tiết kiệm', 1000000, 'Gửi tiết kiệm', 'TK24'),
('GD307', '2025-05-04', 0, 'Gửi tiết kiệm', 1000000, 'Gửi tiết kiệm', 'TK24'),
('GD308', '2025-05-04', 0, 'Gửi tiết kiệm', 1000000, 'Gửi tiết kiệm', 'TK1'),
('GD6', '2025-05-03', 1, 'a', 111000000, 'Nạp tiền', 'TK24');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lichsutichdiem`
--

CREATE TABLE `lichsutichdiem` (
  `MaADB` varchar(10) NOT NULL,
  `ThoiGian` date NOT NULL,
  `DIem` int(11) NOT NULL,
  `MaKH` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `lichsutichdiem`
--

INSERT INTO `lichsutichdiem` (`MaADB`, `ThoiGian`, `DIem`, `MaKH`) VALUES
('ADB001', '2025-05-04', 126318, 'KH1'),
('ADB002', '2024-03-12', 200, 'KH10'),
('ADB003', '2024-02-28', 150, 'KH11'),
('ADB004', '2024-03-08', 120, 'KH12'),
('ADB005', '2024-02-18', 180, 'KH13'),
('ADB006', '2024-01-22', 250, 'KH14'),
('ADB007', '2024-03-03', 130, 'KH15'),
('ADB008', '2024-02-14', 90, 'KH16'),
('ADB009', '2024-03-06', 160, 'KH1'),
('ADB010', '2024-01-25', 110, 'KH1'),
('ADB011', '2024-03-09', 200, 'KH1'),
('ADB012', '2024-03-05', 180, 'KH2'),
('ADB013', '2024-02-17', 140, 'KH2'),
('ADB014', '2024-02-20', 110, 'KH3'),
('ADB015', '2024-02-22', 90, 'KH4'),
('ADB016', '2024-01-15', 150, 'KH5'),
('ADB017', '2024-01-18', 120, 'KH6'),
('ADB018', '2024-03-10', 200, 'KH7'),
('ADB019', '2024-02-25', 170, 'KH8'),
('ADB020', '2024-01-30', 130, 'KH9');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `loaitk`
--

CREATE TABLE `loaitk` (
  `MaLoai` varchar(10) NOT NULL,
  `TenLoai` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `loaitk`
--

INSERT INTO `loaitk` (`MaLoai`, `TenLoai`) VALUES
('ML1', 'Tín dụng'),
('ML2', 'Tiết kiệm'),
('ML3', 'Ghi nợ');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nhanvien`
--

CREATE TABLE `nhanvien` (
  `MaNV` varchar(10) NOT NULL,
  `HoTen` varchar(50) NOT NULL,
  `MaNVQL` varchar(10) NOT NULL,
  `SoCCCD` varchar(20) NOT NULL,
  `SoDienThoai` varchar(10) NOT NULL,
  `isDelete` tinyint(4) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nhanvien`
--

INSERT INTO `nhanvien` (`MaNV`, `HoTen`, `MaNVQL`, `SoCCCD`, `SoDienThoai`, `isDelete`) VALUES
('NV1', 'Nguyễn Văn A', 'NV1', '092200004299', '0975123456', 0),
('NV10', 'Tô Thị J', 'NV6', '010123456789', '0587654321', 0),
('NV11', 'Mỹ Phụngg', 'NV1', '123456789012', '0123456789', 1),
('NV2', 'Trần Thị B', 'NV1', '001234567890', '0367890123', 0),
('NV3', 'Lê Văn C', 'NV1', '003456789012', '0851236789', 0),
('NV4', 'Phạm Thị D', 'NV2', '004567890123', '0912345678', 0),
('NV5', 'Hoàng Văn E', 'NV2', '005678901234', '0384567890', 0),
('NV6', 'Đặng Thị F', 'NV3', '006789012345', '0701234567', 0),
('NV7', 'Bùi Văn G', 'NV3', '007890123456', '0909876543', 0),
('NV8', 'Vũ Thị H', 'NV4', '008901234567', '0398765432', 0),
('NV9', 'Lý Văn I', 'NV5', '009012345678', '0823456789', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quanlycapbac`
--

CREATE TABLE `quanlycapbac` (
  `MaCapBac` varchar(10) NOT NULL,
  `MaNV` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `quanlycapbac`
--

INSERT INTO `quanlycapbac` (`MaCapBac`, `MaNV`) VALUES
('CB1', 'NV1'),
('CB1', 'NV2'),
('CB1', 'NV9'),
('CB2', 'NV10'),
('CB2', 'NV3'),
('CB2', 'NV4'),
('CB3', 'NV5'),
('CB3', 'NV6'),
('CB4', 'NV7'),
('CB4', 'NV8');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `savingssotietkiem`
--

CREATE TABLE `savingssotietkiem` (
  `ID` int(11) NOT NULL,
  `MaTK` varchar(10) DEFAULT NULL,
  `MaKyHan` varchar(10) NOT NULL,
  `SoTienGui` int(11) NOT NULL,
  `NgayMo` date DEFAULT NULL,
  `NgayKetThuc` date DEFAULT NULL,
  `MaTKNguon` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `savingssotietkiem`
--

INSERT INTO `savingssotietkiem` (`ID`, `MaTK`, `MaKyHan`, `SoTienGui`, `NgayMo`, `NgayKetThuc`, `MaTKNguon`) VALUES
(1, 'TK23', 'H1', 111, '2025-05-03', '2025-06-03', 'TK1'),
(5, 'TK27', 'H1', 1000000, '2025-05-04', '2025-06-04', 'TK24'),
(6, 'TK28', 'H1', 1000000, '2025-05-04', '2025-06-04', 'TK24'),
(7, 'TK29', 'H1', 1000000, '2025-05-04', '2025-06-04', 'TK1');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `signature_vectors`
--

CREATE TABLE `signature_vectors` (
  `MaVector` int(11) NOT NULL,
  `MaKH` varchar(10) NOT NULL,
  `vector` longtext NOT NULL,
  `NgayTao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `signature_vectors`
--

INSERT INTO `signature_vectors` (`MaVector`, `MaKH`, `vector`, `NgayTao`) VALUES
(4, 'KH1', '[0.42416873574256897, 0.0, 0.5762045979499817, 0.9592593908309937, 1.9644300937652588, 0.0, 3.6092281341552734, 0.0, 1.5950140953063965, 0.0, 1.4994637966156006, 2.2498433589935303, 0.0, 0.0, 1.2962281703948975, 0.22077588737010956, 1.008523941040039, 0.7247330546379089, 0.0, 2.3982725143432617, 2.2090089321136475, 5.254558563232422, 0.4122047424316406, 0.8328466415405273, 0.0, 2.4513981342315674, 2.692548990249634, 0.0, 0.0, 1.8753658533096313, 0.396890252828598, 0.31432539224624634, 0.0, 1.9809820652008057, 0.0, 0.43051227927207947, 0.25510287284851074, 3.0721707344055176, 0.04918257147073746, 0.08691045641899109, 1.1598565578460693, 5.078464508056641, 0.0, 3.685098171234131, 0.7164298295974731, 0.0, 0.0, 3.1271066665649414, 3.2165398597717285, 2.632582187652588, 1.479511022567749, 0.0, 0.002869639080017805, 5.436667442321777, 0.004025653935968876, 0.03999542444944382, 0.2444993555545807, 0.3449219763278961, 0.0, 4.084566593170166, 3.4068305492401123, 0.6155155301094055, 0.1478879302740097, 3.692103862762451, 1.0731148719787598, 0.5471247434616089, 1.0001146793365479, 0.5670778155326843, 0.5040086507797241, 0.5262857675552368, 1.5394587516784668, 0.7993350028991699, 0.05006089061498642, 1.1368515491485596, 0.4859597682952881, 0.015629392117261887, 2.282829761505127, 0.0, 2.1789791584014893, 0.0, 1.400583267211914, 0.0, 0.0, 0.0, 0.0, 0.9454184770584106, 0.0830107107758522, 0.0, 0.15646052360534668, 0.0, 3.5684866905212402, 1.6074120998382568, 1.7024507522583008, 0.4249575138092041, 0.1554061621427536, 0.19869577884674072, 0.0, 0.953720211982727, 0.20403465628623962, 3.987743377685547, 2.0761475563049316, 0.0, 0.0, 4.171618461608887, 0.47765952348709106, 0.6628473401069641, 0.1650857925415039, 0.027437368407845497, 2.0779824256896973, 0.49579477310180664, 0.947510838508606, 0.5217868089675903, 0.035657528787851334, 1.0778688192367554, 1.7403242588043213, 0.0, 0.3227229714393616, 0.0, 0.0, 2.031552791595459, 0.0, 0.0, 0.0, 2.94024920463562, 0.0, 1.7264989614486694, 1.4438109397888184, 3.6064388751983643, 0.02796160615980625, 0.0, 0.0, 0.0, 0.27807706594467163, 0.0, 2.8945770263671875, 2.485910177230835, 0.9825576543807983, 0.0007449830882251263, 0.0, 0.0, 0.051915861666202545, 0.8845155835151672, 1.1034681797027588, 0.0, 0.0, 0.6692002415657043, 0.0, 0.0, 2.3967814445495605, 0.0, 2.5357470512390137, 1.4962265491485596, 5.22322940826416, 2.360469341278076, 1.2060002088546753, 0.03003097139298916, 1.6116597652435303, 0.49710002541542053, 0.33400464057922363, 0.0, 2.4684910774230957, 0.0, 4.380262851715088, 3.0626683235168457, 1.7746469974517822, 3.194718837738037, 0.0, 4.239187717437744, 0.9457566142082214, 0.883337140083313, 0.49681559205055237, 0.6482008099555969, 1.9402506351470947, 0.0, 0.0, 3.9377224445343018, 0.0, 0.7209316492080688, 0.0, 0.0, 0.0, 1.7498877048492432, 0.0, 0.25125637650489807, 0.0, 0.12678229808807373, 0.0, 3.6205222606658936, 0.0, 4.929767608642578, 0.5639147758483887, 0.7698827385902405, 0.9679681062698364, 3.983633041381836, 0.0, 0.0, 0.893947422504425, 0.49557924270629883, 0.5227418541908264, 2.091993808746338, 2.5369155406951904, 0.0, 0.0, 2.027121067047119, 0.0, 0.4671216905117035, 0.0, 0.0, 0.0, 0.0, 1.1609368324279785, 1.5676500797271729, 0.17310485243797302, 0.0, 3.8732752799987793, 1.9683332443237305, 0.778842568397522, 1.3515089750289917, 1.0901710987091064, 0.0, 0.2528298795223236, 0.0, 0.0, 0.6074331998825073, 1.583794355392456, 0.08889572322368622, 0.09595029056072235, 0.5127884149551392, 2.183875560760498, 4.7234392166137695, 1.1839845180511475, 2.6945509910583496, 0.06422635167837143, 0.3967018127441406, 0.0, 4.74537467956543, 1.010305643081665, 1.7267690896987915, 0.5725025534629822, 2.128770351409912, 2.100461959838867, 0.10530499368906021, 0.0, 1.9938156604766846, 0.7243698239326477, 2.0154404640197754, 2.0256800651550293, 0.6657191514968872, 1.479809284210205, 0.0, 0.5395181775093079, 0.0, 0.0, 3.4511618614196777, 2.7998433113098145, 0.0]', '2025-04-19 11:15:32'),
(5, 'KH17', '[0.0, 0.0, 0.0, 0.1149977594614029, 0.018946819007396698, 0.16143999993801117, 0.12574255466461182, 2.2151970863342285, 0.0, 0.09636762738227844, 0.0, 6.220465660095215, 0.0, 0.0, 0.40271395444869995, 2.341587543487549, 2.3676304817199707, 0.4828616976737976, 0.0, 3.822782039642334, 4.404305934906006, 3.636368989944458, 5.086347579956055, 2.4902939796447754, 2.5015482902526855, 1.0425409078598022, 0.0, 0.5777772068977356, 0.3923181891441345, 0.5426977276802063, 0.3067801892757416, 3.0833144187927246, 0.0, 3.789857864379883, 0.1572904884815216, 0.3295387625694275, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.3163762092590332, 4.06068754196167, 0.0, 0.5812650322914124, 0.0, 0.49391478300094604, 2.862894058227539, 1.4632669687271118, 2.905491590499878, 0.0, 0.12030684947967529, 1.9276195764541626, 0.0, 0.0, 0.0, 0.005884065292775631, 0.0, 0.0, 0.6276870369911194, 0.2769889235496521, 0.0, 0.6661602258682251, 4.228090286254883, 0.0, 3.801579713821411, 0.11197732388973236, 4.285987854003906, 0.8042950630187988, 4.175202369689941, 0.0, 0.0, 1.7445316314697266, 0.19013044238090515, 0.0, 0.2708877921104431, 0.0, 4.96890926361084, 0.0, 0.724380373954773, 0.0, 0.0, 0.21939799189567566, 0.0, 0.059446047991514206, 0.0, 0.0, 1.0882724523544312, 0.0, 0.41166791319847107, 4.710656642913818, 0.5768664479255676, 1.7313988208770752, 0.0, 3.540295124053955, 0.0, 0.0, 3.1650233268737793, 1.5039546489715576, 1.4103333950042725, 0.0, 0.0570254921913147, 4.563201904296875, 0.1676548421382904, 0.34585434198379517, 1.5542439222335815, 2.2030396461486816, 3.0284464359283447, 0.0, 3.4376938343048096, 5.358283519744873, 0.3178066313266754, 0.2506324350833893, 1.014835238456726, 0.0, 1.0358917713165283, 2.0550599098205566, 0.017537064850330353, 7.127394199371338, 0.44808411598205566, 1.2159905433654785, 0.0, 6.341122627258301, 0.0, 2.154754400253296, 1.210676908493042, 3.887256145477295, 2.4442665576934814, 0.0, 0.26050615310668945, 0.0, 0.40847739577293396, 2.702465534210205, 0.0, 3.2378265857696533, 1.314060926437378, 0.0, 0.0, 4.118893146514893, 0.0, 0.0, 0.39730104804039, 0.0, 0.0, 2.6523683071136475, 0.0, 0.0, 3.6320598125457764, 0.0, 5.2045578956604, 0.0, 5.793423175811768, 1.7323001623153687, 1.7563434839248657, 0.0, 1.4767684936523438, 0.0664721354842186, 0.240413099527359, 0.0, 0.0, 0.0, 6.469947814941406, 0.29560744762420654, 2.9474685192108154, 0.0, 0.0, 5.029828071594238, 0.0, 0.7558829188346863, 4.656441688537598, 0.004207701422274113, 2.712484836578369, 0.0, 1.7400829792022705, 0.0, 0.08216467499732971, 0.06054491549730301, 0.0, 0.0, 1.5496292114257812, 0.07290032505989075, 0.0, 0.4881231188774109, 0.1628040373325348, 0.0, 1.5699061155319214, 2.7195076942443848, 0.0, 6.288384437561035, 1.2385402917861938, 2.0501151084899902, 3.4116711616516113, 3.899651288986206, 0.0, 3.3410677909851074, 1.4871671199798584, 0.0, 0.00022946442186366767, 1.1959869861602783, 0.13765987753868103, 0.0, 0.0, 2.916337013244629, 0.0, 1.1631132364273071, 0.0, 0.0, 0.2728123366832733, 0.0, 1.267175316810608, 1.2465964555740356, 2.642839193344116, 0.0, 0.10807617008686066, 2.087592124938965, 0.0, 0.2158680260181427, 1.1767442226409912, 3.2048439979553223, 0.0, 0.0, 0.4784427583217621, 0.6354395151138306, 2.398247241973877, 1.4888935089111328, 3.903900623321533, 0.0, 1.6580778360366821, 1.2965799570083618, 2.715874671936035, 3.23063325881958, 0.0, 0.8165209889411926, 0.0, 1.6820766925811768, 2.348297595977783, 3.0331287384033203, 0.04281815141439438, 0.10979421436786652, 0.9036419987678528, 0.398464560508728, 0.0, 2.3967957496643066, 0.10276806354522705, 1.8120790719985962, 0.8409723043441772, 1.7894618511199951, 0.7505768537521362, 0.0, 1.006666660308838, 0.0, 0.6735583543777466, 5.809592247009277, 0.24748213589191437, 0.0]', '2025-04-19 11:15:34');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `taikhoan`
--

CREATE TABLE `taikhoan` (
  `MaTK` varchar(10) NOT NULL,
  `LoaiTK` varchar(10) NOT NULL,
  `SoDu` int(11) NOT NULL,
  `MaKH` varchar(10) NOT NULL,
  `STK` varchar(50) NOT NULL,
  `NgayDangKy` date NOT NULL,
  `TrangThai` int(2) NOT NULL,
  `ThoiGianDong` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `taikhoan`
--

INSERT INTO `taikhoan` (`MaTK`, `LoaiTK`, `SoDu`, `MaKH`, `STK`, `NgayDangKy`, `TrangThai`, `ThoiGianDong`) VALUES
('TK1', 'ML1', 4203400, 'KH1', '12345678901', '2024-03-01', 1, NULL),
('TK10', 'ML1', 2500000, 'KH6', '55544433322', '2024-03-12', 0, NULL),
('TK11', 'ML3', 17000000, 'KH7', '88899900011', '2024-02-28', 1, NULL),
('TK12', 'ML2', 9000000, 'KH8', '22233344455', '2024-03-08', 1, NULL),
('TK13', 'ML1', 3500000, 'KH9', '11100099988', '2024-02-18', 1, NULL),
('TK14', 'ML2', 11000000, 'KH10', '44433322211', '2024-01-22', 1, NULL),
('TK15', 'ML3', 14000000, 'KH10', '99900011122', '2024-03-03', 1, NULL),
('TK16', 'ML1', 5000000, 'KH11', '66655544433', '2024-02-14', 1, NULL),
('TK17', 'ML2', 7200000, 'KH12', '33322211177', '2024-03-06', 1, NULL),
('TK18', 'ML3', 13000000, 'KH13', '22211100099', '2024-01-25', 1, NULL),
('TK19', 'ML1', 4500000, 'KH14', '11122233355', '2024-03-09', 1, NULL),
('TK2', 'ML2', 5999889, 'KH1', '98765432102', '2024-03-05', 1, NULL),
('TK20', 'ML2', 10500000, 'KH15', '77766655544', '2024-02-17', 1, NULL),
('TK23', 'ML2', 111, 'KH1', '7474851410', '2025-04-30', 1, '0000-00-00 00:00:00'),
('TK24', 'ML1', 109017000, 'KH1', '479003251728', '2025-05-03', 1, NULL),
('TK25', 'ML1', 0, 'KH1', '187167347800', '2025-05-04', 1, NULL),
('TK26', 'ML1', 10000000, 'KH1', '153507695822', '2025-05-04', 1, NULL),
('TK27', 'ML2', 1000000, 'KH1', '2260982991', '2025-05-04', 1, '0000-00-00 00:00:00'),
('TK28', 'ML2', 1000000, 'KH1', '6394407761', '2025-05-04', 1, NULL),
('TK29', 'ML2', 1000000, 'KH1', '0054617058', '2025-05-04', 1, NULL),
('TK3', 'ML1', 3000000, 'KH2', '11122233344', '2024-02-20', 1, NULL),
('TK4', 'ML3', 15000000, 'KH2', '55566677788', '2024-02-22', 1, NULL),
('TK5', 'ML1', 2000000, 'KH3', '99988877766', '2024-01-15', 1, NULL),
('TK6', 'ML2', 8000000, 'KH3', '44455566677', '2024-01-18', 1, NULL),
('TK7', 'ML1', 7500000, 'KH4', '33322211100', '2024-03-10', 1, NULL),
('TK8', 'ML3', 12000000, 'KH4', '66677788899', '2024-02-25', 1, NULL),
('TK9', 'ML2', 6000000, 'KH5', '77788899900', '2024-01-30', 1, NULL);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `accountkh`
--
ALTER TABLE `accountkh`
  ADD PRIMARY KEY (`IdLogin`),
  ADD KEY `MaKH` (`MaKH`);

--
-- Chỉ mục cho bảng `accountnv`
--
ALTER TABLE `accountnv`
  ADD PRIMARY KEY (`IdLogin`),
  ADD KEY `MaNV` (`MaNV`);

--
-- Chỉ mục cho bảng `capbackh`
--
ALTER TABLE `capbackh`
  ADD PRIMARY KEY (`MaCapBac`);

--
-- Chỉ mục cho bảng `chitietkhuyenmai`
--
ALTER TABLE `chitietkhuyenmai`
  ADD PRIMARY KEY (`MaKM`,`MaCapBac`),
  ADD KEY `MaCapBac` (`MaCapBac`);

--
-- Chỉ mục cho bảng `khachhang`
--
ALTER TABLE `khachhang`
  ADD PRIMARY KEY (`MaKH`),
  ADD KEY `MaNVQL` (`MaNVQL`),
  ADD KEY `MaCapBac` (`MaCapBac`);

--
-- Chỉ mục cho bảng `khuyenmai`
--
ALTER TABLE `khuyenmai`
  ADD PRIMARY KEY (`MaKM`),
  ADD KEY `LoaiTKApDung` (`LoaiTKApDung`),
  ADD KEY `fk_capbackh` (`CapBacThanhVien`);

--
-- Chỉ mục cho bảng `kyhan`
--
ALTER TABLE `kyhan`
  ADD PRIMARY KEY (`MaKyHan`);

--
-- Chỉ mục cho bảng `lichsugiaodich`
--
ALTER TABLE `lichsugiaodich`
  ADD PRIMARY KEY (`MaGD`),
  ADD KEY `TKGD` (`TKGD`);

--
-- Chỉ mục cho bảng `lichsutichdiem`
--
ALTER TABLE `lichsutichdiem`
  ADD PRIMARY KEY (`MaADB`),
  ADD KEY `lichsutichdiem_ibfk1` (`MaKH`);

--
-- Chỉ mục cho bảng `loaitk`
--
ALTER TABLE `loaitk`
  ADD PRIMARY KEY (`MaLoai`);

--
-- Chỉ mục cho bảng `nhanvien`
--
ALTER TABLE `nhanvien`
  ADD PRIMARY KEY (`MaNV`),
  ADD KEY `MaNVQL` (`MaNVQL`);

--
-- Chỉ mục cho bảng `quanlycapbac`
--
ALTER TABLE `quanlycapbac`
  ADD PRIMARY KEY (`MaCapBac`,`MaNV`),
  ADD KEY `MaNV` (`MaNV`);

--
-- Chỉ mục cho bảng `savingssotietkiem`
--
ALTER TABLE `savingssotietkiem`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `fk_MaKH` (`MaTK`),
  ADD KEY `MaTKNguon` (`MaTKNguon`),
  ADD KEY `MaKyHan` (`MaKyHan`);

--
-- Chỉ mục cho bảng `signature_vectors`
--
ALTER TABLE `signature_vectors`
  ADD PRIMARY KEY (`MaVector`);

--
-- Chỉ mục cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD PRIMARY KEY (`MaTK`),
  ADD KEY `LoaiTK` (`LoaiTK`),
  ADD KEY `MaKH` (`MaKH`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `savingssotietkiem`
--
ALTER TABLE `savingssotietkiem`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `signature_vectors`
--
ALTER TABLE `signature_vectors`
  MODIFY `MaVector` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `accountkh`
--
ALTER TABLE `accountkh`
  ADD CONSTRAINT `accountkh_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `accountnv`
--
ALTER TABLE `accountnv`
  ADD CONSTRAINT `accountnv_ibfk_1` FOREIGN KEY (`MaNV`) REFERENCES `nhanvien` (`MaNV`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `chitietkhuyenmai`
--
ALTER TABLE `chitietkhuyenmai`
  ADD CONSTRAINT `chitietkhuyenmai_ibfk_1` FOREIGN KEY (`MaCapBac`) REFERENCES `capbackh` (`MaCapBac`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `chitietkhuyenmai_ibfk_2` FOREIGN KEY (`MaKM`) REFERENCES `khuyenmai` (`MaKM`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `khachhang`
--
ALTER TABLE `khachhang`
  ADD CONSTRAINT `khachhang_ibfk_1` FOREIGN KEY (`MaNVQL`) REFERENCES `nhanvien` (`MaNV`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `khachhang_ibfk_2` FOREIGN KEY (`MaCapBac`) REFERENCES `capbackh` (`MaCapBac`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `khuyenmai`
--
ALTER TABLE `khuyenmai`
  ADD CONSTRAINT `fk_capbackh` FOREIGN KEY (`CapBacThanhVien`) REFERENCES `capbackh` (`MaCapBac`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `khuyenmai_ibfk_1` FOREIGN KEY (`LoaiTKApDung`) REFERENCES `loaitk` (`MaLoai`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `lichsugiaodich`
--
ALTER TABLE `lichsugiaodich`
  ADD CONSTRAINT `lichsugiaodich_ibfk_1` FOREIGN KEY (`TKGD`) REFERENCES `taikhoan` (`MaTK`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `lichsutichdiem`
--
ALTER TABLE `lichsutichdiem`
  ADD CONSTRAINT `lichsutichdiem_ibfk1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `nhanvien`
--
ALTER TABLE `nhanvien`
  ADD CONSTRAINT `nhanvien_ibfk_1` FOREIGN KEY (`MaNVQL`) REFERENCES `nhanvien` (`MaNV`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `quanlycapbac`
--
ALTER TABLE `quanlycapbac`
  ADD CONSTRAINT `quanlycapbac_ibfk_1` FOREIGN KEY (`MaCapBac`) REFERENCES `capbackh` (`MaCapBac`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `quanlycapbac_ibfk_2` FOREIGN KEY (`MaNV`) REFERENCES `nhanvien` (`MaNV`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `savingssotietkiem`
--
ALTER TABLE `savingssotietkiem`
  ADD CONSTRAINT `fk_MaKH` FOREIGN KEY (`MaTK`) REFERENCES `taikhoan` (`MaTK`),
  ADD CONSTRAINT `savingssotietkiem_ibfk_1` FOREIGN KEY (`MaTKNguon`) REFERENCES `taikhoan` (`MaTK`),
  ADD CONSTRAINT `savingssotietkiem_ibfk_2` FOREIGN KEY (`MaKyHan`) REFERENCES `kyhan` (`MaKyHan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
