from ..service import search_service

def get_rsapk_by_user(user_name):
    return search_service.get_rsapk_by_user(user_name)

def get_user_info():
    return search_service.get_user_info()