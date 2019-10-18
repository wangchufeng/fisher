from flask import Blueprint, render_template

# 把蓝图注册放到__init__下面来，可以让一个蓝图注册多个视图函数，达到将视图函数分解成多个模块
web = Blueprint("web", __name__, template_folder="templates")


# 通过@web.app_errorhandler(404)，来捕获全局的404异常信息
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
from app.web import hello


