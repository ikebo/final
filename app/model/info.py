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

    def __init__(self, realName, oneScore, twoScore, threeScore):
        self.realName = realName
        self.oneScore = oneScore
        self.twoScore = twoScore
        self.threeScore = threeScore
        self.avgScore = (oneScore+twoScore+threeScore)/3.0

    def __repr__(self):
        return '{}: {}'.format(self.realName, self.avgScore)