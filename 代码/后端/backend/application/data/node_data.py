from ..models.node import Node
from ..utils.mysql import db

def get_node_list():
    return Node.query.all()

def insert_node(node_name,node_ip,node_type,node_note,node_state,node_time):
    node_info = Node(node_name,node_ip,node_type,node_note,node_state,node_time)
    db.session.add(node_info)
    db.session.commit()
    db.session.close()

def change_node_state_by_ip(node_ip,new_state):
    user_info = Node.query.filter_by(NODE_IP=node_ip)
    user_info.update({'NODE_STATE': new_state})
    db.session.commit()
    db.session.close()