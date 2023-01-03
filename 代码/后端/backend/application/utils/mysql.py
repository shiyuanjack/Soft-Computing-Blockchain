from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..configs import config

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()

from ..models import user,admin,node 

def init_mysql(app:Flask):
    # 加载配置文件
    app.config.from_object(config)
    # db绑定app
    db.init_app(app)

    manager = Manager(app)
    Migrate(app=app, db=db)
    manager.add_command('db', MigrateCommand) # 创建数据库映射命令
    manager.add_command('start', Server(port=8000, use_debugger=True)) # 创建启动命令

    # manager.run()

