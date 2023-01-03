import base64
from struct import pack
from ..service import upload_service
from ..utils.des_tool import *
import json
import rsa
import ipfshttpclient
from ..configs import config

def upload_log_json_to_IPFS(log_json:json):
    ipfs_api = ipfshttpclient.connect()
    return ipfs_api.add_json(json.dumps(log_json))

def package_log_file(user_name,date1,date2,file_path):
    key_info = upload_service.get_user_key_info(user_name)
    des_key = getKey(key_info['des'])
    public_key = key_info['pk']
    private_key = key_info['sk']
    encrypt_data = dict()
    encrypt_data['date1'] = date1
    encrypt_data['date2'] = date2
    with open(file_path,'r',encoding='utf-8') as f:
        encrypt_data['content'] = f.read()
    encrypted_data = Encrption(json.dumps(encrypt_data),des_key)
    signature  = rsa.sign(encrypted_data, rsa.PrivateKey.load_pkcs1(private_key.encode()),'SHA-256')
    package_info = dict()
    package_info["encrypted_data"] = base64.b64encode(encrypted_data).decode()
    package_info["signature"] = base64.b64encode(signature).decode()
    package_info["publickey"] = public_key
    package_info["logtime"] = date1 + " " + date2
    return package_info

def package_log_json(user_name,date1,date2,clientIP,email,name,requestmethod,code,number,note):
    key_info = upload_service.get_user_key_info(user_name)
    des_key = getKey(key_info['des'])
    public_key = key_info['pk']
    private_key = key_info['sk']
    encrypt_data = dict()
    encrypt_data['date1'] = date1
    encrypt_data['date2'] = date2
    encrypt_data['clientIP'] = clientIP
    encrypt_data['email'] = email
    encrypt_data['name'] = name
    encrypt_data['requestmethod'] = requestmethod
    encrypt_data['code'] = code
    encrypt_data['number'] = number
    encrypt_data['note'] = note
    encrypted_data = Encrption(json.dumps(encrypt_data),des_key)
    signature  = rsa.sign(encrypted_data, rsa.PrivateKey.load_pkcs1(private_key.encode()),'SHA-256')
    package_info = dict()
    package_info["encrypted_data"] = base64.b64encode(encrypted_data).decode()
    package_info["signature"] = base64.b64encode(signature).decode()
    package_info["publickey"] = public_key
    package_info["logtime"] = date1 + " " + date2
    return package_info

    
    
    # 密文解密
    # package_info["plaint"] = DeEncrption(base64.b64decode(package_info["encrypted_data"].encode()),des_key)
    # 验签
    # package_info["verify"] = rsa.verify(base64.b64decode(package_info["encrypted_data"].encode()), 
                    # base64.b64decode(package_info["signature"].encode()),
                    # rsa.PublicKey.load_pkcs1(package_info["publickey"].encode()))
    #上传数据到IPFS
    # hash_tags = upload_log_json_to_IPFS(json.dumps(package_info))

def package_log_string(log_string,date1,date2,user_name):
    key_info = upload_service.get_user_key_info(user_name)
    des_key = getKey(key_info['des'])
    public_key = key_info['pk']
    private_key = key_info['sk']
    encrypt_data = dict()
    encrypt_data['logString'] = log_string
    
    encrypted_data = Encrption(json.dumps(encrypt_data),des_key)

    signature  = rsa.sign(encrypted_data, rsa.PrivateKey.load_pkcs1(private_key.encode()),'SHA-256')

    package_info = dict()
    package_info["encrypted_data"] = base64.b64encode(encrypted_data).decode()
    package_info["signature"] = base64.b64encode(signature).decode()
    package_info["publickey"] = public_key
    package_info["logtime"] = date1 + " " + date2

    return package_info