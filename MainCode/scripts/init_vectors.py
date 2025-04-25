import sys
import os

# Thêm đường dẫn thư mục gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.init_signature import initialize_signature_vectors
from app import app  # import Flask app từ app.py

if __name__ == "__main__":
    with app.app_context():  # Đặt trong context của Flask
        initialize_signature_vectors()
