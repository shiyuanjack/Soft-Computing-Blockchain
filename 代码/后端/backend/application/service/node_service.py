from tkinter.tix import DirTree
from ..data import node_data

def add_node(node_name,node_ip,node_type,node_note,node_state,node_time):
    node_data.insert_node(node_name,node_ip,node_type,node_note,node_state,node_time)

def change_node_state(node_ip,new_state):
    node_data.change_node_state_by_ip(node_ip,new_state)

def get_node_list():
    node_info = node_data.get_node_list()
    unread_list = []
    read_list = []
    recycle_list = []
    for node in node_info:
        node_temp = dict()
        node_temp["nodeid"] = node.NODE_ID
        node_temp["nodename"] = node.NODE_NAME
        node_temp["nodeip"] = node.NODE_IP
        node_temp["nodetype"] = node.NODE_TYPE
        node_temp["nodenote"] = node.NODE_NOTE
        node_temp["nodestate"] = node.NODE_STATE
        node_temp["nodetime"] = node.NODE_TIME
        if(node_temp["nodestate"] == "申请"):
            unread_list.append(node_temp)
        elif(node_temp["nodestate"] == "已通过"):
            read_list.append(node_temp)
        elif(node_temp["nodestate"] == "未通过"):
            recycle_list.append(node_temp)
    return (unread_list,read_list,recycle_list)