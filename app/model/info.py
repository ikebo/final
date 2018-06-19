import os

from flask import url_for

from app import app
from app.utils.log import Log
from . import db

class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realName = db.Column(db.String(80))
    oneScore = db.Column(db.Integer)
    twoScore = db.Column(db.Integer)
    threeScore = db.Column(db.Integer)
    avgScore = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img = db.Column(db.String(200))

    def __init__(self, user_id, realName='未填写', oneScore=-1, twoScore=-1, threeScore=-1):
        self.user_id = user_id
        self.realName = realName
        self.oneScore = oneScore
        self.twoScore = twoScore
        self.threeScore = threeScore
        self.avgScore = (oneScore+twoScore+threeScore)/3.0 if not \
            oneScore == 1 and twoScore == 1 and threeScore == 1 else -1
        ra = app.config['DEFAULT_IMG'].rsplit('\\',2)
        # url_for  与 os.path.join 混用的话会出讲'\'转义
        self.img = url_for('static', filename=(ra[-2]+'/'+ra[-1]))
        # self.img = os.path.join('\\static',ra[-2],ra[-1])

    def update_info(self, kwargs):
        self.realName = kwargs['realName']
        self.oneScore = int(kwargs['oneScore']) if not kwargs['oneScore'] == '未填写' else -1
        self.twoScore = int(kwargs['twoScore']) if not kwargs['twoScore'] == '未填写' else -1
        self.threeScore = int(kwargs['threeScore']) if not kwargs['threeScore'] == '未填写' else -1
        self.avgScore = (self.oneScore+self.twoScore+self.threeScore)/3
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '{}: {}'.format(self.realName, self.avgScore)