from ..models.admin import Admin
from ..utils.mysql import db

def get_admin_by_name(admin_name):
    return Admin.query.filter_by(ADMIN_NAME=admin_name).first()

def insert_admin(user_name,user_password_hash):
    admin_info = Admin(user_name,user_password_hash)
    db.session.add(admin_info)
    db.session.commit()
    db.session.close()