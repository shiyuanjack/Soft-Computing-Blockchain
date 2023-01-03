import json
import os
import threading
from struct import pack_into
import time
from flask import Flask, jsonify, make_response, render_template, send_file
from flask import request
from flask_cors import CORS, cross_origin
import requests
from sqlalchemy import true
from application.configs import config
from application.service import search_service

from application.utils import mysql,email_tool
from application.control import register_control
from application.control import login_control
from application.control import change_pwd_control
from application.control import upload_control
from application.control import serch_control
from application.control import download_control
from application.control import node_control

app = Flask(__name__)
cors = CORS(app,supports_credentials=True)

@app.route('/')
def hello_world():
    #app.logger.info(login.get_the_password(123)) 
    return '123'

@cross_origin()
@app.route('/register', methods=['POST', 'GET'])
def user_register():
    info = dict()
    info['register_result'] = "false"
    if request.method == 'POST':
        if email_tool.verifyMailCode(request.json['useremail'], request.json['verifycode']) and \
                                            register_control.user_register(request.json['registername'],
                                            request.json['registerpassword'],
                                            request.json['useremail'],
                                            request.json['userphone'],
                                            request.json['deskey'],
                                            request.json['rsapk'],
                                            request.json['rsask'],
                                            0):
            info['register_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/getcode', methods=['POST', 'GET'])
def get_code():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        if email_tool.sendMailCode(request.json['useremail']):
            info['get_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/adminRegister', methods=['POST', 'GET'])
def admin_register():
    info = dict()
    info['register_result'] = "false"
    if request.method == 'POST':
        if register_control.admin_register(request.json['registername'],request.json['registerpassword']):
            info['register_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/login', methods=['POST', 'GET'])
def user_login():
    info = dict()
    info['login_result'] = "false"
    if request.method == 'POST':
        login_id,user_permit = login_control.valid_login(request.json['name'], request.json['password'])
        if  login_id != 'None':
            info['login_info'] = login_id
            if(login_id == 'user'):
                info['user_permit'] = user_permit
            info['login_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/generateRSA')
def generate_rsa():
    rsa_info = register_control.generate_rsa()
    return jsonify(rsa_info)

@cross_origin()
@app.route('/changePassword', methods=['POST', 'GET'])
def change_password():
    info = dict()
    info['changeresult'] = "false"
    if request.method == 'POST':
        if( email_tool.verifyMailCode(request.json['useremail'], request.json['verifycode']) and \
                change_pwd_control.change_password_by_email(request.json['cname'], request.json['newpassword'], request.json['useremail'])):
            info['changeresult'] = "true"
    return jsonify(info)


def up_log_json_to_IPFS_blockchain(package_info):
    payload = dict()
    payload['hash_tags']= upload_control.upload_log_json_to_IPFS(json.dumps(package_info))
    payload['logtime']=package_info['logtime']
    payload['rsapk']=package_info['publickey']
    json.loads(requests.post("http://{0}:{1}/uploadLog".format(config.CHAINHOST,config.CHAINPROT),json=payload).text)

@cross_origin()
@app.route('/uploadLogJson', methods=['POST', 'GET'])
def upload_log_json():
    info = dict()
    info['upload_result'] = "false"
    if request.method == 'POST':
        if(request.json['resource'] == 'json'):
            package_info = upload_control.package_log_json(request.json['uploadname'],
                                                request.json['date1'],
                                                request.json['date2'],
                                                request.json['clientIP'],
                                                request.json['email'],
                                                request.json['name'],
                                                request.json['requestmethod'],
                                                request.json['code'],
                                                request.json['number'],
                                                request.json['note'])
            obj1 = threading.Thread(target=up_log_json_to_IPFS_blockchain ,args=(package_info,))
            obj1.start()
        elif(request.json['resource'] == '字符串'):
            package_info = upload_control.package_log_string(request.json['stringlog'],
                                                request.json['date1'],
                                                request.json['date2'],
                                                request.json['uploadname'])
            obj1 = threading.Thread(target=up_log_json_to_IPFS_blockchain ,args=(package_info,))
            obj1.start()
        info['upload_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/uploadLogFile', methods=['POST', 'GET'])
def upload_log_file():
    info = dict()
    info['upload_result'] = "false"
    if request.method == 'POST':
        save_path = os.path.join('data')
        attfile = request.files.get('file')
        attfile.save(os.path.join(save_path, attfile.filename))
        package_info = upload_control.package_log_file(request.form['uploadname'],
                                        request.form['date1'],
                                        request.form['date2'],
                                        os.path.join(save_path, attfile.filename))
        obj1 = threading.Thread(target=up_log_json_to_IPFS_blockchain ,args=(package_info,))
        obj1.start()
        info['upload_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/searchLog', methods=['POST', 'GET'])
def search_log():
    info = dict()
    info['search_result'] = "false"
    if request.method == 'POST':
        payload = dict()
        payload['starttime'] = request.json['starttime']
        payload['endtime'] = request.json['endtime']
        payload['pk'] =  search_service.get_rsapk_by_user(request.json['name'])
        search_response =  json.loads(requests.post("http://{0}:{1}/searchLog".format(config.CHAINHOST,config.CHAINPROT),json=payload).text)
        info['search_response_bc'] = search_response
        info['search_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/searchLogAdmin', methods=['POST', 'GET'])
def search_log_admin():
    info = dict()
    info['search_result'] = "false"
    if request.method == 'POST':
        payload = dict()
        payload['starttime'] = request.json['starttime']
        payload['endtime'] = request.json['endtime']
        search_response =  json.loads(requests.post("http://{0}:{1}/searchLogAdmin".format(config.CHAINHOST,config.CHAINPROT),json=payload).text)
        info['search_response_bc'] = search_response
        info['search_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/getIPFSLog', methods=['POST', 'GET'])
def get_ipfs_log():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        ipfs_data = json.loads(json.loads(download_control.download_log_json_from_IPFS(request.json['ipfs'])))
        info['encrypted_data'] = ipfs_data['encrypted_data']
        info['decrypted_data'] = download_control.get_pliant(info['encrypted_data'],request.json['pk'])
        info['signature'] = ipfs_data['signature']
        info['publickey'] = ipfs_data['publickey']
        info['logtime'] = ipfs_data['logtime']
        info['get_result'] = "true"
    return jsonify(info)

@app.route('/downLoadjsonLog',  methods=['POST', 'GET'])
@cross_origin()
def download_json_log():
    info = dict()
    info['download_result'] = "false"
    if request.method == 'POST':
        path =  download_control.downoad_log_json_txt(request.json['ipfs'],request.json['pk'])
        return send_file(path,as_attachment=True)
    return make_response(jsonify(info))

@app.route('/getNowTxs',  methods=['POST', 'GET'])
@cross_origin()
def get_now_txs():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        payload = dict()
        payload['number'] = request.json['number']
        json_data = json.loads(requests.post("http://{0}:{1}/getNowTxs".format(config.CHAINHOST,config.CHAINPROT),json=payload).text)
        info['list'] = json_data['list']
        info['txNumber'] = json_data['txNumber']
        info['get_result'] = "true"
    info['get_result'] = "true"
    return jsonify(info)

@app.route('/getBlocks',  methods=['POST', 'GET'])
@cross_origin()
def get_blocks():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        payload = dict()
        payload['number'] = request.json['number']
        info['list'] = json.loads(requests.post("http://{0}:{1}/getBlocks".format(config.CHAINHOST,config.CHAINPROT),json=payload).text)['list']
        info['get_result'] = "true"
    info['get_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/getUserInfo', methods=['POST', 'GET'])
def get_user_info():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        info['list'] = serch_control.get_user_info()
        info['get_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/changeUserPermit', methods=['POST', 'GET'])
def change_user_permit():
    info = dict()
    info['change_result'] = "false"
    if request.method == 'POST':
        change_pwd_control.change_permit_by_name(request.json['name'],request.json['permit'])
        info['change_result'] = "true"
    return jsonify(info)

def get_time_by_mktime(_mktime):
    log_time =  time.localtime(int(float(_mktime)))
    return str(log_time.tm_year) + '-' + str(log_time.tm_mon).rjust(2,'0') + '-' + str(log_time.tm_mday).rjust(2,'0') + ' ' + \
            str(log_time.tm_hour).rjust(2,'0') + ':' + str(log_time.tm_min).rjust(2,'0') + ':' + str(log_time.tm_sec).rjust(2,'0')

@cross_origin()
@app.route('/addNode', methods=['POST', 'GET'])
def add_node():
    info = dict()
    info['add_result'] = "false"
    if request.method == 'POST':
        nodetime = str(time.time())
        nodestate = "申请"
        node_control.add_node(request.json['nodename'],request.json['nodeip'],request.json['nodetype'],request.json['nodenote'],
                        nodestate,get_time_by_mktime(nodetime))
        info['add_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/getNode', methods=['POST', 'GET'])
def get_node_list():
    info = dict()
    info['get_result'] = "false"
    if request.method == 'POST':
        unread_list,read_list,recycle_list = node_control.get_node_list()
        info["unreadData"] = unread_list
        info["readData"] = read_list
        info["recycleData"] = recycle_list
        info['get_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/changeNodeState', methods=['POST', 'GET'])
def change_node_state():
    info = dict()
    info['change_result'] = "false"
    if request.method == 'POST': 
        node_control.change_node_state(request.json['nodeip'],request.json['nodestate'])
        info['change_result'] = "true"
    return jsonify(info)

@cross_origin()
@app.route('/getNodeState', methods=['POST', 'GET'])
def get_node_state():
    info = dict()
    info['get_result'] = "false"
    info['nodelist']  = node_control.get_node_list_state()
    info['get_result'] = "true"
    return jsonify(info)

if __name__ == '__main__':
    # 建表命令
    # python main.py db init
    # python main.py db migrate
    # python main.py db upgrade
    mysql.init_mysql(app)
    app.run(debug=True)


