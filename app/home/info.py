from flask import session, render_template, request, flash, redirect, url_for

from app.model.info import Info
from app.model.user import User
from app import db
from . import home


@home.route('/me')
def me():
    info = Info.query.filter_by(user_id=session['userId']).first()
    return render_template('home/me.html',info=info, round=round)

@home.route('/edit', methods=['GET','POST'])
def edit():
    info = Info.query.filter_by(user_id=session['userId']).first()
    if request.method == 'POST':
        if info.update_info(request.form):
            flash('修改成功！')
            return redirect(url_for('home.me'))
    else:
        return render_template('home/edit.html',info=info)