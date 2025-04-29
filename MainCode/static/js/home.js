async function validateForm(event) {
    event.preventDefault();

    const fields = [
        { id: 'hoten', pattern: /^[a-zA-ZÀ-ỹ\s]+$/, error: 'Họ tên chỉ chứa chữ cái và dấu cách' },
        { id: 'cccd', pattern: /^\d{12}$/, error: 'CCCD phải có đúng 12 chữ số' },
        { id: 'noicapcccd', pattern: /^[\p{L}\s]+$/u, error: 'Nơi cấp CCCD chỉ chứa chữ cái và dấu cách' },
        { id: 'quoctich', pattern: /^[\p{L}\s]+$/u, error: 'Quốc tịch chỉ chứa chữ cái và dấu cách' },
        { id: 'noicutru', pattern: /^[\p{L}\d\s,.-]+$/u, error: 'Nơi cư trú không hợp lệ' },
        { id: 'diachithuongtru', pattern: /^[\p{L}\d\s,.-]+$/u, error: 'Địa chỉ thường trú không hợp lệ' },
        { id: 'sodienthoai', pattern: /^0\d{9}$/, error: 'Số điện thoại phải có 10 chữ số và bắt đầu bằng 0' },
        { id: 'email', pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, error: 'Email không hợp lệ' },
        { id: 'ngaysinh', pattern: /^\d{4}-\d{2}-\d{2}$/, error: 'Ngày sinh phải có định dạng YYYY-MM-DD' },
        { id: 'ngaycapcccd', pattern: /^\d{4}-\d{2}-\d{2}$/, error: 'Ngày cấp CCCD phải có định dạng YYYY-MM-DD' },
        { id: 'cogiatriden', pattern: /^\d{4}-\d{2}-\d{2}$/, error: 'Có giá trị đến phải có định dạng YYYY-MM-DD' },
        { id: 'dantoc', pattern: /^[\p{L}\s]+$/u, error: 'Dân tộc chỉ chứa chữ cái và dấu cách' },
        { id: 'diachihientai', pattern: /^[\p{L}\d\s,.-]+$/u, error: 'Địa chỉ hiện tại không hợp lệ' },
        { id: 'gioitinh', pattern: /^(Nam|Nữ|Khác)$/, error: 'Giới tính chỉ có thể là Nam, Nữ hoặc Khác' },
        { id: 'nghenghiep', pattern: /^[\p{L}\s]+$/u, error: 'Nghề nghiệp chỉ chứa chữ cái và dấu cách' }
    ];
    

    let isValid = true;

    fields.forEach(field => {
        const input = document.getElementById(field.id);
        const errorElement = document.getElementById(field.id + '-error');

        if (!input || !errorElement) return; // Nếu không tìm thấy phần tử, bỏ qua

        if (!field.pattern.test(input.value)) {
            errorElement.textContent = field.error;
            isValid = false;
        } else {
            errorElement.textContent = ''; // Xóa lỗi nếu hợp lệ
        }
    });
    // Kiểm tra trùng trong CSDL nếu dữ liệu đã hợp lệ
    if (isValid) {
        const soCCCD = document.getElementById('cccd').value; // Lấy giá trị của CCCD
        const soDienThoai = document.getElementById('sodienthoai').value; // Lấy giá trị của Số điện thoại
        
        const response = await fetch("/admin/kiemTraTrung", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                SoCCCD: soCCCD,
                SoDienThoai: soDienThoai,
            }),
        });
        
        const result = await response.json();

        if (result.trungCCCD) {
            document.getElementById("cccd").classList.add("is-invalid");
            document.getElementById("cccd-error").innerText = "Số CCCD đã tồn tại.";
            isValid = false;
        }

        if (result.trungSDT) {
            document.getElementById("sodienthoai").classList.add("is-invalid");
            document.getElementById("sodienthoai-error").innerText = "Số điện thoại đã tồn tại.";
            isValid = false;
        }
    }

    // Nếu hợp lệ thì submit form
    if (isValid) {
        event.target.submit();  // Dùng event.target thay cho this.submit() để đảm bảo đúng đối tượng
    }
}
