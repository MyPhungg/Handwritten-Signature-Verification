
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/bank"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "hiden"  # Dùng để mã hóa session
