import os

from app import app

SQLALCHEMY_DATABASE_URI = r'sqlite:///final.sqlite3'
SECRET_KEY = 'final'

# 上传文件
UPLOAD_FOLDER = os.path.join(app.static_folder,'uploads')
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

# 最大 1M
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

# 默认头像
DEFAULT_IMG = os.path.join(app.static_folder,'images','default.png')