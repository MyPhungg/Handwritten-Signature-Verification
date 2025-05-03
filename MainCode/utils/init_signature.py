import os
from routes.auth import save_mean_signature_vector, get_vector_from_db

def initialize_signature_vectors():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'signatures'))
    for ma_kh in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, ma_kh)
        if os.path.isdir(folder_path):
            if get_vector_from_db(ma_kh) is None:
                if any(f.lower().endswith(('.png', '.jpg', '.jpeg')) for f in os.listdir(folder_path)):
                    print(f"[INFO] Đang xử lý chữ ký cho khách hàng: {ma_kh}")
                    save_mean_signature_vector(folder_path,ma_kh)
                else:
                    print(f"[WARNING] Không có ảnh hợp lệ cho {ma_kh}")
            else:
                print(f"[OK] Vector cho {ma_kh} đã tồn tại")

