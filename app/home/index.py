from app.utils.log import Log
from . import home
from flask import render_template, request, flash, session, redirect, url_for
from app.model.user import User
from app.forms.user import LoginForm

@home.route('/', methods=['GET','POST'])
def index():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # return '{}:{}'.format(request.form['username'], request.form['password'])
        user = User.query_by_login(form.username.data,form.password.data)
        return '{}'.format(user)
        if user == True:
            session['username'] = form.username.data
            flash('Logged in as {}'.format(form.username.data))
        else:
            errorMsg = user
            flash(errorMsg, category='login_error')
            # return render_template('home/index.html', form=form)
    return render_template('home/index.html',form=form)
