import base64
from pyDes import *

Des_IV = b"\x52\x63\x78\x61\xBC\x48\x6A\x07" # 自定IV向量

def Encrption(str,Des_Key):
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(str))
 
def DeEncrption(str,Des_Key):
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(str))

def getKey(des_key):
    if(len(des_key) < 8):
        des_key = des_key.ljust(8,'0')
    if(len(des_key) > 8):
        des_key = des_key[:8]
    return des_key