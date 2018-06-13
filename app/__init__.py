from flask import Flask

app = Flask(__name__)
app.config.from_object('app.settings')

# 创建数据库
from app.model import db
with app.app_context():
    db.init_app(app)
    db.create_all()

# 注册蓝图
from app.home import home as home_blueprint
app.register_blueprint(home_blueprint)
