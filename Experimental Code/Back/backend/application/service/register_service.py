import base64
from encodings import utf_8
from ..data import user_data,admin_data
import rsa

def find_user(user_name):
    user_info = user_data.get_user_by_name(user_name)
    if(user_info != None):
        return True
    else:
        return False


def find_admin(user_name):
    admin_info = admin_data.get_admin_by_name(user_name)
    if(admin_info != None):
        return True
    else:
        return False

def insert_user(user_name,user_password_hash,user_email,user_phone,user_des_hash,user_rsapk,user_rsask,permit):
    user_data.insert_user(user_name,user_password_hash,user_email,user_phone,user_des_hash,user_rsapk,user_rsask,permit)

def insert_admin(user_name,user_password_hash):
    admin_data.insert_admin(user_name,user_password_hash)

def generate_rsa():
    (public_key, private_key) = rsa.newkeys(2048)
    key_pair = dict()
    key_pair['public_key'] = public_key.save_pkcs1().decode()
    key_pair['private_key'] = private_key.save_pkcs1().decode()
    return key_pair
