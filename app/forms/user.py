from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, NoneOf, ValidationError, AnyOf

from app.model.user import User
from app.utils.log import Log


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message='用户名不能为空！')])
    password = PasswordField('password', validators=[DataRequired(message='密码不能为空！')])


class RegisterForm(LoginForm):
    repassword = StringField('repassword', validators=[DataRequired(message='请确认密码！')])


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

    def validate_repassword(self,field):
        if field.data != self.password.data:
            raise ValidationError('两次密码不一致！')
