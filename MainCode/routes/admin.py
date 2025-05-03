from flask import Blueprint, jsonify, render_template, flash, request, redirect, url_for, session
from models import NhanVien, db, KhachHang, QuanLyCapBac
from sqlalchemy import cast, or_
from sqlalchemy.types import Integer
from sqlalchemy.sql import func
admin_bp = Blueprint('admin', __name__)

# Lấy danh sách nhân viên


@admin_bp.route('/nhanvien', methods=['GET', 'POST'])
def loadDanhSachNhanVien():
    list = sortListFromDB(NhanVien, "MaNV")
    return render_template('/admin/NhanVien.html', list=list, isSearch=False)

# Xem chi tiết 1 nhân viên


@admin_bp.route('/nhanvien/chitiet/<maNV>', methods=['GET', 'POST'])
def chiTietNhanVien(maNV):
    nhanvien = NhanVien.query.get(maNV)
    ds_quanly = NhanVien.query.filter_by(isDelete=0).all()
    if not nhanvien:
        flash('Không tìm thấy nhân viên này!', 'error')
        return redirect(url_for('admin.loadDanhSachNhanVien'))
    return render_template('/admin/chitietNhanVien.html', nhanvien=nhanvien, ds_quanly=ds_quanly)

# sửa nhân viên


@admin_bp.route('/nhanvien/sua/<maNV>', methods=['GET', 'POST'])
def suaNhanVien(maNV):
    nhanvien = NhanVien.query.get(maNV)
    if nhanvien and nhanvien.isDelete == 0:
        if request.method == 'POST':
            nhanvien.HoTen = request.form.get('HoTen')
            nhanvien.SoDienThoai = request.form.get('SoDienThoai')
            nhanvien.SoCCCD = request.form.get('SoCCCD')
            nhanvien.MaNVQL = request.form.get('maNVQL')

            db.session.commit()
        flash('Cập nhật thông tin nhân viên thành công!', 'success')
        return redirect(url_for('admin.chiTietNhanVien', maNV=maNV))

    else:
        flash('Không tìm thấy nhân viên này!', 'error')
        return redirect(url_for('admin.loadDanhSachNhanVien'))


# chuyển đến trang thêm nhân viên


@admin_bp.route('/nhanvien/goToAddStaff')
def goToAddStaff():
    list = NhanVien.query.all()
    return render_template('admin/themNhanVien.html', list=list)

# sắp xếp danh sách theo thứ tự mã nhân viên tăng dần


def sortListFromDB(model, primarykey):
    column = getattr(model, primarykey)
    list = model.query.filter_by(isDelete=0).order_by(
        cast(func.substr(column, 3), Integer)
    ).all()
    return list

# Thêm nhân viên


@admin_bp.route('/nhanvien/them', methods=['POST'])
def themNhanVien():
    goToAddStaff()
    # Đếm số lượng nhân viên hiện có
    so_luong_nv = NhanVien.query.count()
    ma_nv_moi = f"NV{so_luong_nv + 1}"

    # Lấy dữ liệu từ form
    ho_ten = request.form['HoTen']
    ma_quan_ly = request.form['MaNguoiQuanLy']
    so_cccd = request.form['SoCCCD']
    so_dien_thoai = request.form['SoDienThoai']

    # Tạo đối tượng nhân viên mới
    nv_moi = NhanVien(
        MaNV=ma_nv_moi,
        HoTen=ho_ten,
        MaNVQL=ma_quan_ly,
        SoCCCD=so_cccd,
        SoDienThoai=so_dien_thoai
    )

    # Lưu vào cơ sở dữ liệu
    db.session.add(nv_moi)
    db.session.commit()

    return redirect(url_for('admin.loadDanhSachNhanVien'))

# Tìm kiếm


@admin_bp.route('/nhanvien/timkiem', methods=['GET'])
def timKiem():
    keyword = request.args.get('keyword', '')
    if keyword:
        list = NhanVien.query.filter(
            or_(
                NhanVien.MaNV.contains(keyword),
                NhanVien.HoTen.contains(keyword),
                NhanVien.SoCCCD.contains(keyword),
                NhanVien.SoDienThoai.contains(keyword),
            )
        ).order_by(
            cast(func.substr(NhanVien.MaNV, 3), Integer)
        ).all()
        return render_template('admin/NhanVien.html', list=list, isSearch=True, keyword=keyword)

    else:
        list = sortListFromDB(NhanVien, "MaNV")
        return render_template('/admin/NhanVien.html', list=list, isSearch=False)

# xóa nhân viên


@admin_bp.route('/nhanvien/xoa', methods=['POST'])
def xoaNhanVien():
    maNVs = request.form.getlist('xoaNhanVien')
    if maNVs:
        for ma in maNVs:
            nv = NhanVien.query.get(ma)
            if nv:
                # Đang quản lý nhân viên khác?
                dangQuanLyNhanVien = NhanVien.query.filter_by(
                    MaNVQL=nv.MaNV, isDelete=0).first()

                # Đang quản lý khách hàng nào không?
                dangQuanLyKhachHang = KhachHang.query.filter_by(
                    MaNVQL=nv.MaNV).first()

                # Đang quản lý cấp bậc?
                dangQuanLyCapBac = QuanLyCapBac.query.filter_by(
                    MaNV=nv.MaNV).first()

                if not dangQuanLyNhanVien and not dangQuanLyKhachHang and not dangQuanLyCapBac:
                    nv.isDelete = 1
                    flash(f'Đã sa thải nhân viên {ma} thành công!', 'success')
                else:
                    flash(
                        f'Nhân viên {ma} chưa hoàn tất bàn giao công việc nên không thể sa thải!', 'error')
                    return render_template('admin/NhanVien.html',
                                           list=sortListFromDB(
                                               NhanVien, "MaNV"),
                                           checked_maNVs=maNVs,
                                           isSearch=False)
        db.session.commit()
    return redirect(url_for('admin.loadDanhSachNhanVien'))


# Kiểm tra trùng
@admin_bp.route('/kiemTraTrung', methods=['POST'])
def kiemTraTrung():
    data = request.json
    soCCCD = data.get('SoCCCD')
    soDienThoai = data.get('SoDienThoai')
    maNV = data.get('MaNV')
    if (maNV):
        cccd_trung = db.session.query(NhanVien).filter(
            NhanVien.SoCCCD == soCCCD, NhanVien.MaNV != maNV).first()
        sdt_trung = db.session.query(NhanVien).filter(
            NhanVien.SoDienThoai == soDienThoai, NhanVien.MaNV != maNV).first()
    else:
        maKH = session['MaKH']
        cccd_trung = db.session.query(KhachHang).filter(
            KhachHang.SoCCCD == soCCCD, KhachHang.MaKH != maKH).first()
        sdt_trung = db.session.query(KhachHang).filter(
            KhachHang.SoDienThoai == soDienThoai, KhachHang.MaKH != maKH).first()

    return jsonify({
        "trungCCCD": cccd_trung is not None,
        "trungSDT": sdt_trung is not None
    })
