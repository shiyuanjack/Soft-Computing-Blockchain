from pickle import TRUE
from sqlalchemy import true
from ..utils.mysql import db
from werkzeug.security import generate_password_hash, check_password_hash

class Node(db.Model):
    __tablename__ = 'node_table'
    __table_args__ = {'extend_existing': True}
    NODE_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NODE_NAME = db.Column(db.String(15), nullable=False)
    NODE_IP = db.Column(db.String(128), nullable=False)
    NODE_TYPE = db.Column(db.String(15), nullable=False)
    NODE_NOTE = db.Column(db.String(15))
    NODE_STATE = db.Column(db.String(128), nullable=False)
    NODE_TIME = db.Column(db.String(128), nullable=False)

    def __init__(self, node_name,node_ip,node_type,node_note,node_state,node_time):
        self.NODE_NAME = node_name
        self.NODE_IP = node_ip
        self.NODE_TYPE = node_type
        self.NODE_NOTE = node_note
        self.NODE_STATE = node_state
        self.NODE_TIME = node_time