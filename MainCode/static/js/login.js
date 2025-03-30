// Login.htmml
function goToChooseAcc(){
    window.location.href = "./chooseAcc.html";
}
function goHome() {
    window.location.href = "./user/home.html";
}
function goForgetAcc() {
    window.location.href = "./forgetAcc.html";
}
function goForgetPass() {
    window.location.href = "./forgetPass.html";
}

// forgetAcc & Pass
function showCCCD() {
    document.getElementById("cccdForm").style.display = "block";
    document.getElementById("signatureForm").style.display = "none";
}

function showSignature() {
    document.getElementById("cccdForm").style.display = "none";
    document.getElementById("signatureForm").style.display = "block";
}

function goBack() {
    window.location.href = "./login.html";
}
function showResult() {
    document.getElementById("inputForm").style.display = "none";
    document.getElementById("signatureForm").style.display = "none";
    document.getElementById("resultForm").style.display = "block";
}

//Home.html
function goInfoUser(){
    window.location.href = "./infoUser.html";

}

// Regex
function validateFormForgetAcc(event) {
    event.preventDefault();

    const fields = [
        { id: 'cccd', pattern: /^\d{12}$/, error: 'CCCD phải có đúng 12 chữ số!' },
        { id: 'phonenumber', pattern: /^0\d{9}$/, error: 'Số điện thoại phải có 10 chữ số và bắt đầu bằng 0!' },
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
    if (isValid) {
        event.target.submit();
    }
}

function validateFormForgetPass(event) {
    event.preventDefault();

    const fields = [
        { id: 'cccd', pattern: /^\d{12}$/, error: 'CCCD phải có đúng 12 chữ số!' },
        { id: 'username', pattern: /^[a-zA-Z][a-zA-Z0-9._]{2,19}$/, error: 'Tên đăng nhập không hợp lệ!'}    
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
    if (isValid) {
        event.target.submit();
    }
}