from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message='用户名不能为空!')])
    password = PasswordField('password', validators=[DataRequired(message='密码不能为空!')])