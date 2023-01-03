import json
from ..data import user_data

def get_rsapk_by_user(user_name):
    user_info = user_data.get_user_by_name(user_name)
    return user_info.USER_RSAPK

def get_user_info():
    user_info = user_data.get_user_list()
    user_list = []
    for user in user_info:
        user_temp = dict()
        user_temp['uid'] = user.USER_ID
        user_temp['name'] = user.USER_NAME
        user_temp['email'] = user.USER_EAMIL
        user_temp['phone'] = user.USER_PHONE
        user_temp['publickKey'] = user.USER_RSAPK
        if(user.USER_PERMIT == 0):
            user_temp['permit'] = "读写"
        if(user.USER_PERMIT == 1):
            user_temp['permit'] = "只读"
        if(user.USER_PERMIT == 2):
            user_temp['permit'] = "只写"
        user_list.append(user_temp)
    return user_list