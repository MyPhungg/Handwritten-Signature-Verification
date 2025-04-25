
from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.account import account_bp
from routes.home import home_bp
from routes.admin import admin_bp


def create_app():

    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")
    app.config.from_object(Config)

    db.init_app(app)

    # Tạo bảng nếu chưa có
    with app.app_context():
        db.create_all()

    # Đăng ký Blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(home_bp, url_prefix='/home')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
