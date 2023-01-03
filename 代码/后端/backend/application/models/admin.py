from ..utils.mysql import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin_table'
    __table_args__ = {'extend_existing': True}
    ADMIN_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ADMIN_NAME = db.Column(db.String(15), nullable=False)
    ADMIN_PASSWORD = db.Column(db.String(128), nullable=False)

    def __init__(self, user_name,user_password_hash):
        self.ADMIN_NAME = user_name
        self.ADMIN_PASSWORD = user_password_hash

    def set_password(self, password):
        self.ADMIN_PASSWORD = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.ADMIN_PASSWORD, password)