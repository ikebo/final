from app.model.info import Info
from app.utils.utils import generate_md5
from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(120))
    info = db.relationship('Info', backref='user',
                           uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        info = Info(self.id)
        db.session.add(info)
        db.session.commit()
        self.info = info


    @staticmethod
    def query_by_login(username,password):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return 'user does not exist!'
        else:
            user = User.query.filter_by(username=username,password=password).first()
            xuser = User.query.filter_by(username=username,password=generate_md5(password)).first()
            if user is None and xuser is None:
                return 'password does not correct!'
            else:
                return xuser if user is None else user


    def __repr__(self):
        return '<User %r>' % self.username

