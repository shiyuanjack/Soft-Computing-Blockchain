from ..models.user import User
from ..utils.mysql import db

def get_user_by_name(user_name):
    return User.query.filter_by(USER_NAME=user_name).first()
    
def get_user_by_pk(pk):
    return User.query.filter_by(USER_RSAPK=pk).first()


def insert_user(user_name,user_password_hash,user_email,user_phone,user_des_hash,user_rsapk,user_rsask,permit):
    user_info = User(user_name,user_password_hash,user_email,user_phone,user_des_hash,user_rsapk,user_rsask,permit)
    db.session.add(user_info)
    db.session.commit()
    db.session.close()

def change_user_password_by_name(user_name, new_password):
    user_info = User.query.filter_by(USER_NAME=user_name)
    user_info.update({'USER_PASSWORD': new_password})
    db.session.commit()
    db.session.close()

def get_user_list():
    return User.query.all()

def change_user_permit_by_name(user_name,new_permit):
    user_info = User.query.filter_by(USER_NAME=user_name)
    user_info.update({'USER_PERMIT': new_permit})
    db.session.commit()
    db.session.close()
    

