from ..models import user
from ..service import login_service
from werkzeug.security import generate_password_hash, check_password_hash

def valid_login(user_name, password):
    if login_service.find_user(user_name):
        if(check_password_hash(login_service.get_user_password(user_name),password)):
            return ('user',login_service.get_user_permit(user_name))
        else:
            return ('None','None')
    elif login_service.find_admin(user_name):
        if(check_password_hash(login_service.get_admin_password(user_name),password)):
            return ('admin','None')
        else:
            return ('None','None')
    else:
        return ('None','None')

def log_the_user_in(user_name):
    return user_name
