-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th3 20, 2025 lúc 11:43 AM
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
('KM1', 'CB1'),
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
('KH1', 'Nguyễn Văn A', '1995-06-15', '123456789012', '2020-01-01', 'Hà Nội', '2030-01-01', 'Việt Nam', 'Kinh', 'Hà Nội', 'Hà Nội', 'Hà Nội', 'Nam', '0123456789', 'Kinh doanh', 'a@gmail.com', 'NV1', 'CB1'),
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
('KH4', 'Phạm Thị D', '1985-05-05', '321321321321', '2017-04-15', 'Cần Thơ', '2027-04-15', 'Việt Nam', 'Kinh', 'Cần Thơ', 'Cần Thơ', 'Cần Thơ', 'Nữ', '0912121212', 'Giáo viên', 'd@gmail.com', 'NV10', 'CB2'),
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
  `GiaTriKM` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `khuyenmai`
--

INSERT INTO `khuyenmai` (`MaKM`, `NoiDung`, `ThoiGian`, `LoaiTKApDung`, `LoaiKM`, `GiaTriKM`) VALUES
('KM1', 'Tăng lãi suất cho tài khoản Tiết kiệm', '2025-04-01', 'ML2', 'Tăng', 1),
('KM10', 'Giảm lãi suất vay cho khách hàng lâu năm (Tín dụng)', '2025-05-15', 'ML1', 'Giảm', 3),
('KM2', 'Giảm lãi suất vay cho tài khoản Tín dụng', '2025-04-05', 'ML1', 'Giảm', 2),
('KM3', 'Tăng lãi suất khi gửi trên 500 triệu với tài khoản Tiết kiệm', '2025-04-10', 'ML2', 'Tăng', 1),
('KM4', 'Giảm phí rút tiền trước hạn cho tài khoản Tiết kiệm', '2025-04-15', 'ML2', 'Giảm', 2),
('KM5', 'Tăng lãi suất cho tài khoản Tiết kiệm từ 1 tỷ', '2025-04-20', 'ML2', 'Tăng', 2),
('KM6', 'Giảm lãi suất vay cho tài khoản Ghi nợ', '2025-04-25', 'ML3', 'Giảm', 1),
('KM7', 'Tăng lãi suất khi gửi từ 2 tỷ với tài khoản Tiết kiệm', '2025-04-30', 'ML2', 'Tăng', 3),
('KM8', 'Giảm phí duy trì tài khoản Tín dụng', '2025-05-05', 'ML1', 'Giảm', 1),
('KM9', 'Tăng lãi suất khi tái gửi với tài khoản Tiết kiệm', '2025-05-10', 'ML2', 'Tăng', 2);

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
  `MaNVQL` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nhanvien`
--

INSERT INTO `nhanvien` (`MaNV`, `HoTen`, `MaNVQL`) VALUES
('NV1', 'Nguyễn Văn A', 'NV1'),
('NV10', 'Tô Thị J', 'NV6'),
('NV2', 'Trần Thị B', 'NV1'),
('NV3', 'Lê Văn C', 'NV1'),
('NV4', 'Phạm Thị D', 'NV2'),
('NV5', 'Hoàng Văn E', 'NV2'),
('NV6', 'Đặng Thị F', 'NV3'),
('NV7', 'Bùi Văn G', 'NV3'),
('NV8', 'Vũ Thị H', 'NV4'),
('NV9', 'Lý Văn I', 'NV5');

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
-- Cấu trúc bảng cho bảng `taikhoan`
--

CREATE TABLE `taikhoan` (
  `MaTK` varchar(10) NOT NULL,
  `LoaiTK` varchar(10) NOT NULL,
  `SoDu` int(11) NOT NULL,
  `MaKH` varchar(10) NOT NULL,
  `STK` varchar(50) NOT NULL,
  `NgayDangKy` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `taikhoan`
--

INSERT INTO `taikhoan` (`MaTK`, `LoaiTK`, `SoDu`, `MaKH`, `STK`, `NgayDangKy`) VALUES
('TK1', 'ML1', 5000000, 'KH1', '12345678901', '2024-03-01'),
('TK10', 'ML1', 2500000, 'KH6', '55544433322', '2024-03-12'),
('TK11', 'ML3', 17000000, 'KH7', '88899900011', '2024-02-28'),
('TK12', 'ML2', 9000000, 'KH8', '22233344455', '2024-03-08'),
('TK13', 'ML1', 3500000, 'KH9', '11100099988', '2024-02-18'),
('TK14', 'ML2', 11000000, 'KH10', '44433322211', '2024-01-22'),
('TK15', 'ML3', 14000000, 'KH10', '99900011122', '2024-03-03'),
('TK16', 'ML1', 5000000, 'KH11', '66655544433', '2024-02-14'),
('TK17', 'ML2', 7200000, 'KH12', '33322211177', '2024-03-06'),
('TK18', 'ML3', 13000000, 'KH13', '22211100099', '2024-01-25'),
('TK19', 'ML1', 4500000, 'KH14', '11122233355', '2024-03-09'),
('TK2', 'ML2', 10000000, 'KH1', '98765432102', '2024-03-05'),
('TK20', 'ML2', 10500000, 'KH15', '77766655544', '2024-02-17'),
('TK3', 'ML1', 3000000, 'KH2', '11122233344', '2024-02-20'),
('TK4', 'ML3', 15000000, 'KH2', '55566677788', '2024-02-22'),
('TK5', 'ML1', 2000000, 'KH3', '99988877766', '2024-01-15'),
('TK6', 'ML2', 8000000, 'KH3', '44455566677', '2024-01-18'),
('TK7', 'ML1', 7500000, 'KH4', '33322211100', '2024-03-10'),
('TK8', 'ML3', 12000000, 'KH4', '66677788899', '2024-02-25'),
('TK9', 'ML2', 6000000, 'KH5', '77788899900', '2024-01-30');

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
  ADD KEY `LoaiTKApDung` (`LoaiTKApDung`);

--
-- Chỉ mục cho bảng `lichsugiaodich`
--
ALTER TABLE `lichsugiaodich`
  ADD PRIMARY KEY (`MaGD`),
  ADD KEY `TKGD` (`TKGD`);

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
-- Chỉ mục cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD PRIMARY KEY (`MaTK`),
  ADD KEY `LoaiTK` (`LoaiTK`),
  ADD KEY `MaKH` (`MaKH`);

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
  ADD CONSTRAINT `khuyenmai_ibfk_1` FOREIGN KEY (`LoaiTKApDung`) REFERENCES `loaitk` (`MaLoai`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `lichsugiaodich`
--
ALTER TABLE `lichsugiaodich`
  ADD CONSTRAINT `lichsugiaodich_ibfk_1` FOREIGN KEY (`TKGD`) REFERENCES `taikhoan` (`MaTK`) ON DELETE CASCADE ON UPDATE CASCADE;

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
-- Các ràng buộc cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD CONSTRAINT `taikhoan_ibfk_1` FOREIGN KEY (`LoaiTK`) REFERENCES `loaitk` (`MaLoai`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `taikhoan_ibfk_2` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
