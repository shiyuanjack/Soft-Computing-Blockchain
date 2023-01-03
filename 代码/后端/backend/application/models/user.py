from ..utils.mysql import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user_table'
    __table_args__ = {'extend_existing': True}
    USER_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    USER_NAME = db.Column(db.String(15), nullable=False)
    USER_PASSWORD = db.Column(db.String(128), nullable=False)
    USER_EAMIL = db.Column(db.String(15), nullable=False)
    USER_PHONE = db.Column(db.String(15), nullable=False)
    USER_DES = db.Column(db.String(128), nullable=False)
    USER_RSAPK = db.Column(db.String(1000), nullable=False)
    USER_RSASK = db.Column(db.String(2500), nullable=False)
    USER_PERMIT = db.Column(db.Integer, nullable=False)

    def __init__(self, user_name,user_password_hash,user_email,user_phone,user_des_hash,user_rsapk,user_rsask,permit):
        self.USER_NAME = user_name
        self.USER_PASSWORD = user_password_hash
        self.USER_EAMIL = user_email
        self.USER_PHONE = user_phone
        self.USER_DES = user_des_hash
        self.USER_RSAPK = user_rsapk
        self.USER_RSASK = user_rsask
        self.USER_PERMIT = permit

    def set_password(self, password):
        self.USER_PASSWORD = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.USER_PASSWORD, password)

    def set_des(self,des):
        self.USER_DES = generate_password_hash(des)

    def validate_des(self,des):
        return check_password_hash(self.USER_DES, des)