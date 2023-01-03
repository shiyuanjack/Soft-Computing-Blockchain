from ..data import user_data

def get_user_info_by_user_name(user_name):
    user_info = user_data.get_user_by_name(user_name)
    return user_info

def change_pwd_by_user_name(user_name,new_password):
    user_data.change_user_password_by_name(user_name,new_password)

def change_permit_by_name(user_name,new_permit):
    user_data.change_user_permit_by_name(user_name,new_permit)