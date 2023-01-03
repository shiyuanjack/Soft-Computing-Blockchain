import json
import requests
from ..service import node_service

def add_node(node_name,node_ip,node_type,node_note,node_state,node_time):
    node_service.add_node(node_name,node_ip,node_type,node_note,node_state,node_time)

def get_node_list():
    return node_service.get_node_list()

def get_node_list_state():
    unread_list,read_list,recycle_list = node_service.get_node_list()
    node_state_list = []
    for read_node in read_list:
        try:
            res_json = json.loads(requests.post("http://{0}:4396/chainState".format(read_node['nodeip']),data={},timeout=1).text)
            if(res_json['chain_state'] == 'running'):
                read_node['nodestate'] = '运行'
            else:
                read_node['nodestate'] = '停止'
        except:
            read_node['nodestate'] = '停止'
        finally:
            node_state_list.append(read_node)
    return node_state_list
            

def change_node_state(node_ip,new_state):
    node_service.change_node_state(node_ip,new_state)