from werkzeug.exceptions import RequestEntityTooLarge

from app.model.info import Info
from app.utils.log import Log
from app.utils.utils import allowed_file, get_fileRoute, generate_md5
from . import home
from flask import render_template, request, flash, session, redirect, url_for
from app.model.user import User
from app.forms.user import LoginForm, RegisterForm
from app import db, app
from werkzeug.utils import secure_filename

@home.route('/', methods=['GET','POST'])
@home.route('/<int:page>', methods=['GET','POST'])
def index(page=1):
    target = request.args.get('target',None)
    if not target:
        pagination = Info.query.order_by(Info.avgScore.desc()).paginate(page,per_page=5,error_out=False)
        infos = pagination.items
    else:
        pagination = Info.query.filter(Info.realName.like('%{}%'.format(target))).order_by(Info.avgScore.desc()).paginate(page,per_page=2,error_out=False)
        infos = pagination.items
        flash('搜索结果')
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query_by_login(form.username.data,form.password.data)
        if type(user) != str:
            session['userId'] = user.id
            flash('Logged in as {}'.format(form.username.data))
            return redirect(url_for('home.index'))
        else:
            errorMsg = user
            flash(errorMsg, category='login_error')
            return redirect(url_for('home.index'))
    # 传入form用于显示error信息
    return render_template('home/index.html',form=form,infos=infos,round=round,pagination=pagination)


@home.route('/logout')
def logout():
    session.pop('userId')
    flash('logged out')
    return redirect(url_for('home.index'))


@home.route('/register', methods=['GET', 'POST'])
@home.route('/register/<int:page>')
def register(page=1):
    form = RegisterForm(request.form)
    pagination = Info.query.order_by(Info.avgScore.desc()).paginate(page, per_page=5, error_out=False)
    infos = pagination.items
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,generate_md5(form.password.data))
        db.session.add(user)
        db.session.commit()
        session['userId'] = user.id
        flash('注册成功，已自动登录！')
        return redirect(url_for('home.index'))
    return render_template('home/index.html',form=form, register=True, infos=infos, round=round, pagination=pagination)


@home.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                path = get_fileRoute(filename)
                file.save(path)
                ra = path.rsplit('\\',3)
                r = url_for('static', filename=(ra[-3]+'/'+ra[-2]+'/'+ra[-1]))
                user = User.query.get(session['userId'])
                user.info.img = r
                db.session.add(user.info)
                db.session.commit()
            except RequestEntityTooLarge as e:
                flash('the size of img is too large!')
                return redirect(request.url)
            flash('upload successfully')
    return redirect(url_for('home.me'))