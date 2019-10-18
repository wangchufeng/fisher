from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from app.models.book import Book
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


def create_app():
	app = Flask(__name__)
	app.config.from_object('app.secure')  # 载入config.py配置文件
	app.config.from_object('app.setting')
	register_blueprint(app)

	db.init_app(app)
	login_manager.init_app(app)
	# 把登陆的视图函数的endpoint赋值给login_view,这样flask-login就知道没有登入的时候，跳转到哪个页面
	login_manager.login_view = 'web.login'
	mail.init_app(app)
	# app.app_context表示应用上下文
	# create_all需要获取app核心对象，在create_all的内部代码中判断current_app是否存在，
	# 所以用with app.app_context()将应用上下文推入栈（看源码，__enter__），然后可以找到app的核心对象了
	with app.app_context():
		db.create_all()
	return app


#   应用上下文  AppContext
# 	current_app指向栈最顶元素的核心对象，每当有request的请求，flask会判断是否有应用上下文在栈中
#   如果没有，则推入。所以在没有request的请求的情况下，需要手动推入应用上下文.

def register_blueprint(app):
	from app.web import web
	app.register_blueprint(web)

