from flask import session, render_template, request, flash, redirect, url_for

from app.model.info import Info
from app.model.user import User
from app import db
from app.utils.log import Log
from app.utils.utils import generate_subject
from . import home


@home.route('/me')
def me():
    info = Info.query.filter_by(user_id=session['userId']).first()
    change = request.args.get('change',None)
    return render_template('home/me.html',info=info,round=round,change=change)

@home.route('/edit', methods=['GET','POST'])
def edit():
    info = Info.query.filter_by(user_id=session['userId']).first()
    if request.method == 'POST':
        if info.update_info(request.form):
            flash('修改成功！')
            return redirect(url_for('home.me'))
    else:
        return render_template('home/edit.html',info=info)


@home.route('/about')
def about():
    return render_template('home/about.html')


@home.route('/order')
def order():
    subjects = []
    oneSubject = generate_subject('C',db.session.query(Info.oneScore).order_by(Info.oneScore.desc()).all())
    twoSubject = generate_subject('C++',db.session.query(Info.twoScore).order_by(Info.twoScore.desc()).all())
    threeSubject = generate_subject('Python',db.session.query(Info.threeScore).order_by(Info.threeScore.desc()).all())
    subjects.append(oneSubject)
    subjects.append(twoSubject)
    subjects.append(threeSubject)
    subjects.sort(key= lambda x: x.avgScore, reverse=True)
    return render_template("home/order.html",subjects=subjects)