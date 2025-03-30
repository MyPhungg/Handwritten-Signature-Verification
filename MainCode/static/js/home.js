function validateForm() {
    // Lấy giá trị từ form
    const hoten = document.getElementById('hoten').value;
    const cccd = document.getElementById('cccd').value;
    const sodienthoai = document.getElementById('sodienthoai').value;
    const email = document.getElementById('email').value;

    // Regex patterns (giống với backend)
    const patterns = {
        hoten: /^[a-zA-ZÀ-ỹ\s]+$/,
        cccd: /^\d{12}$/,
        sodienthoai: /^0\d{9}$/,
        email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
        ngaysinh: /^\d{4}-\d{2}-\d{2}$/
    };

    // Validate từng trường
    if (!patterns.hoten.test(hoten)) {
        alert('Họ tên chỉ được chứa chữ cái và dấu cách');
        return false;
    }

    if (!patterns.cccd.test(cccd)) {
        alert('CCCD phải có đúng 12 chữ số');
        return false;
    }

    if (!patterns.sodienthoai.test(sodienthoai)) {
        alert('Số điện thoại phải bắt đầu bằng 0 và có 10 chữ số');
        return false;
    }

    if (!patterns.email.test(email)) {
        alert('Email không hợp lệ');
        return false;
    }

    return true; // Submit form nếu validate thành công
}