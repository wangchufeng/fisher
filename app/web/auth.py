from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, logout_user

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from app.libs.email import send_email

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # login_user将用户信息写入cookie，下面写法是一次性cookie，
            # 即关闭浏览器就删除cookie，需要定时设置可查阅flask-login文档
            login_user(user)
            # request.args能获取到路由？后面的参数（http://localhost:5000/login?next=%2Fmy%2Fgifts）
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # 找不到数据时候，fisrt_or_404会抛出一个异常（异常抛出后面代码不执行），通过try可以自己定义返回页面
            # 这里采用AOP思想，集中处理404异常，（web/__init__.py下面定义）
            user = User.query.filter_by(email=account_email).first_or_404()
            send_email(form.email.data, '重置你的密码',
                       'email/reset_password.html', user=user, token=user.generate_token())
            flash('一封邮件已发送到邮箱'+account_email+'， 请及时查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已经更新，请使用新密码登陆')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
