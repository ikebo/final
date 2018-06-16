from flask import session, render_template

from app.model.info import Info
from app.model.user import User
from app import db
from . import home


@home.route('/me')
def me():
    info = Info.query.filter_by(user_id=session['userId']).first()
    if info is None:
        info = Info()
        db.session.add(info)
        db.session.commit()
    return render_template('home/me.html',info=info)