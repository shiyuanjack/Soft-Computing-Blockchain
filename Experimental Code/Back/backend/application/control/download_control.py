import json
import os
import ipfshttpclient
from ..utils.des_tool import *
from ..data import user_data
from flask import make_response, send_file

def download_log_json_from_IPFS(hash_tags):
    ipfs_api = ipfshttpclient.connect()
    return ipfs_api.get_json(hash_tags)

def get_pliant(encrypted_data,pk):
    user_info = user_data.get_user_by_pk(pk)
    # user_info = user_data.get_user_by_name(user_name)
    des_key = getKey(user_info.USER_DES)
    # return json.loads(DeEncrption(base64.b64decode(encrypted_data.encode()),des_key).decode())
    return DeEncrption(base64.b64decode(encrypted_data.encode()),des_key).decode()

def downoad_log_json_txt(ipfs,pk):
    ipfs_data =  json.loads(json.loads(download_log_json_from_IPFS(ipfs)))
    encrypted_data = ipfs_data['encrypted_data']
    pliant = get_pliant(encrypted_data,pk)
    path = os.path.join("data",ipfs + ".txt")
    with open(path,'w',encoding='utf-8') as f:
        f.write(pliant)
        #json.dump(pliant, f,ensure_ascii=False)
    return path