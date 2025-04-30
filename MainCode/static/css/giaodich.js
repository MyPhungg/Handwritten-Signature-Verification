document.getElementById("transaction-btn").addEventListener("click", function() {
    document.getElementById("transaction-history").classList.toggle("hidden");
    loadTransactions();  // Gọi hàm tải giao dịch khi click vào "Lịch sử giao dịch"
});

document.getElementById("saving-btn").addEventListener("click", function() {
    document.getElementById("saving-modal").style.display = "flex";
});

document.getElementById("close-modal").addEventListener("click", function() {
    document.getElementById("saving-modal").style.display = "none";
});

// Tải danh sách giao dịch từ Flask
async function loadTransactions() {
const response = await fetch('api/lichsugiaodich');  // Sử dụng 127.0.0.1 thay vì localhost
const transactions = await response.json();
console.log("Transactions loaded:", transactions); // Kiểm tra dữ liệu trong console
const tableBody = document.querySelector("#transaction-table tbody");
transactions.forEach(transaction => {
const row = document.createElement("tr");
 // Kiểm tra dữ liệu trong console

// Thêm lớp income hoặc expense tùy theo ChieuGD
const directionClass = transaction.ChieuGD === 1 ? "income" : "expense";

row.innerHTML = `
    <td class="transaction-id">${transaction.id}</td>
    <td class="transaction-date">${transaction.NgayGD}</td>
    <td class="transaction-direction ${directionClass}">${transaction.ChieuGD === 1 ? 'Tiền vào' : 'Tiền ra'}</td>
    <td class="${directionClass}">${transaction.GiaTriGD.toLocaleString()}</td>
`;
tableBody.appendChild(row);
});
}

async function fetchDataAndRenderCharts() {
try {
const response = await fetch('http://127.0.0.1:5000/thongke');
if (!response.ok) {
    throw new Error('Network response was not ok');
}
const data = await response.json();
console.log("Data received:", data); // Kiểm tra dữ liệu trong console

// Vẽ biểu đồ doanh thu
const ctxRevenue = document.getElementById('revenueChart').getContext('2d');
new Chart(ctxRevenue, {
    type: 'line',
    data: {
        labels: data.months, // Sửa từ chartData.months thành data.months
        datasets: [{
            label: 'Tiền vào (triệu VND)',
            data: data.money_in, // Sửa từ chartData.money_in thành data.money_in
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
        }, {
            label: 'Tiền ra (triệu VND)',
            data: data.money_out, // Sửa từ chartData.money_out thành data.money_out
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Biểu đồ thu chi theo tháng'
            }
        }
    }
});

// Biểu đồ tiết kiệm
const ctxSavings = document.getElementById('savingsChart').getContext('2d');
new Chart(ctxSavings, {
    type: 'line',
    data: {
        labels: data.years, // Sửa từ chartData.years thành data.years
        datasets: [{
            label: 'Số dư tiết kiệm (triệu VND)',
            data: data.savings_growth, // Sửa từ chartData.savings_growth thành data.savings_growth
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Biểu đồ tăng trưởng tiết kiệm'
            }
        }
    }
});

} catch (error) {
console.error('Error fetching data:', error);
}
}
// Gọi hàm để lấy dữ liệu và vẽ biểu đồ khi trang được tải
fetchDataAndRenderCharts();


document.addEventListener('DOMContentLoaded', () => {
const modal = document.getElementById('saving-modal');
const openBtn = document.getElementById('saving-btn');
const closeBtn = document.getElementById('close-modal');
const interestRateSpan = document.getElementById('interest-rate');
const termSelect = document.getElementById('term');
const balanceSpan = document.getElementById('balance'); // Hiển thị số dư
const amountInput = document.getElementById('amount');

const makh = 'KH01';  // Giả lập MaKH. Cần lấy từ session nếu có đăng nhập.

// Mở modal
openBtn.addEventListener('click', () => {
modal.style.display = 'block';
getBalance(); // Lấy số dư khi mở modal
});

// Đóng modal khi bấm nút close
closeBtn.addEventListener('click', () => {
modal.style.display = 'none';
});

// Đóng modal khi click bên ngoài modal
window.addEventListener('click', (event) => {
if (event.target === modal) modal.style.display = 'none';
});

// Cập nhật lãi suất theo kỳ hạn khi thay đổi option
termSelect.addEventListener('change', () => {
const selectedOption = termSelect.options[termSelect.selectedIndex];
const rate = selectedOption.getAttribute('data-rate');
interestRateSpan.textContent = rate + '%';
});

// Lấy số dư tài khoản từ server
function getBalance() {
fetch(`/get_balance/${makh}`)
.then(res => res.json())
.then(data => {
if (data.balance !== undefined) {
balanceSpan.textContent = data.balance + " VND";
}
})
.catch(err => console.error(err));
}


// Gửi request mở sổ tiết kiệm
function submitSaving() {
const amount = amountInput.value;
const term = termSelect.value;

if (!amount || amount < 1000000) {
alert("Vui lòng nhập số tiền hợp lệ (tối thiểu 1.000.000 VND)");
return;
}

fetch('/mo_sotietkiem', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
MaKH: makh,
SoTienGui: amount,
KyHan: term
})
})
.then(res => res.json())
.then(data => {
alert(data.message);
modal.style.display = 'none';
getBalance(); // Cập nhật lại số dư sau khi mở sổ tiết kiệm
})
.catch(err => {
console.error(err);
alert("Lỗi khi mở sổ tiết kiệm");
});
}

// Gắn sự kiện submit cho nút mở sổ tiết kiệm trong modal
document.querySelector('.saving-modal-content button').addEventListener('click', submitSaving);
});



document.getElementById("expense-btn").addEventListener("click", () => {
fetch('/api/expense-chart-data')
.then(response => response.json())
.then(data => {
    console.log(data);  // In ra dữ liệu để kiểm tra
    const labels = data.map(item => item.category);
    const values = data.map(item => item.total);
    const colors = labels.map(() => '#' + Math.floor(Math.random()*16777215).toString(16));

    const ctx = document.getElementById('expense-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Tỷ lệ chi tiêu theo danh mục'
                }
            }
        }
    });

    document.getElementById('chart-container').style.display = 'block';
})
.catch(error => {
    console.error('Lỗi khi lấy dữ liệu:', error);
    document.getElementById('chart-container').style.display = 'block';
console.log('Chart container shown');

});
});


// Khi nhấn vào nút đóng, ẩn biểu đồ
document.getElementById("close-btn").addEventListener("click", () => {
document.getElementById("chart-container").style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
const dichVuButton = document.querySelector(".nav-link.dropdown-toggle");
const servicesMenu = document.querySelector(".dropdown-menu");

if (dichVuButton && servicesMenu) {
dichVuButton.addEventListener("click", function(event) {
    event.preventDefault(); // Ngăn chặn hành động mặc định
    servicesMenu.classList.toggle("show"); // Toggle dropdown
});
}
});