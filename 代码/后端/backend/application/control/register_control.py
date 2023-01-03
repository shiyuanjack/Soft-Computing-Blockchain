from ..service import register_service
from werkzeug.security import generate_password_hash, check_password_hash

def user_register(user_name,user_password,user_email,user_phone,user_des,user_rsapk,user_rsask,permit):
    if(register_service.find_user(user_name) or register_service.find_admin(user_name)):
        return False
    else:
        user_password_hash = generate_password_hash(user_password)
        #user_des_hash = generate_password_hash(user_des)
        register_service.insert_user(user_name,user_password_hash,user_email,user_phone,user_des,user_rsapk,user_rsask,permit)
        return True

def admin_register(user_name,user_password):
    if(register_service.find_user(user_name) or register_service.find_admin(user_name)):
        return False
    else:
        user_password_hash = generate_password_hash(user_password)
        #user_des_hash = generate_password_hash(user_des)
        register_service.insert_admin(user_name,user_password_hash)
        return True


def generate_rsa():
    return register_service.generate_rsa()