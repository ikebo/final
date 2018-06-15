from app.utils.log import Log
from . import home
from flask import render_template, request, flash, session, redirect, url_for
from app.model.user import User
from app.forms.user import LoginForm

@home.route('/', methods=['GET','POST'])
def index():
    Log(session)
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query_by_login(form.username.data,form.password.data)
        if user == True:
            session['username'] = form.username.data
            flash('Logged in as {}'.format(form.username.data))
            return redirect(url_for('home.index'))
        else:
            errorMsg = user
            flash(errorMsg, category='login_error')
            return redirect(url_for('home.index'))
    # 传入form用于显示error信息
    return render_template('home/index.html',form=form)


@home.route('/logout')
def logout():
    session.pop('username')
    flash('logged out')
    return redirect(url_for('home.index'))