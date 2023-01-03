from ..data import user_data

def get_user_key_info(user_name):
    user_info = user_data.get_user_by_name(user_name)
    key_info = dict()
    key_info['des'] = user_info.USER_DES
    key_info['pk'] = user_info.USER_RSAPK
    key_info['sk'] = user_info.USER_RSASK
    return key_info