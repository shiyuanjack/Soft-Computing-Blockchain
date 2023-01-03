from ..data import user_data,admin_data

def get_user_permit(user_name):
    user_info = user_data.get_user_by_name(user_name)
    return user_info.USER_PERMIT

def get_user_password(user_name):
    user_info = user_data.get_user_by_name(user_name)
    if(user_info != None):
        return user_info.USER_PASSWORD
    else:
        return None

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

def get_admin_password(user_name):
    admin_info = admin_data.get_admin_by_name(user_name)
    if(admin_info != None):
        return admin_info.ADMIN_PASSWORD
    else:
        return None
