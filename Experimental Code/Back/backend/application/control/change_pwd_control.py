from ..models import user
from ..service import change_pwd_service
from werkzeug.security import generate_password_hash, check_password_hash

def change_password_by_email(user_name,new_password,user_email):
    user_info = change_pwd_service.get_user_info_by_user_name(user_name)
    if(user_info == None):
        return False
    elif(user_info.USER_EAMIL != user_email):
        return False
    else:
        change_pwd_service.change_pwd_by_user_name(user_name,generate_password_hash(new_password))
        return True

def change_permit_by_name(user_name,new_permit):
    if (new_permit == '读写'):
        new_permit = 0
    if (new_permit == '只读'):
        new_permit = 1
    if (new_permit == '只写'):
        new_permit = 2
    change_pwd_service.change_permit_by_name(user_name,new_permit)