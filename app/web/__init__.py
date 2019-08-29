from flask import Blueprint

# 把蓝图注册放到__init__下面来，可以让一个蓝图注册多个视图函数，达到将视图函数分解成多个模块
web = Blueprint("web", __name__)
