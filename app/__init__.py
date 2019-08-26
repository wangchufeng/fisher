from flask import Flask


def create_app():
	app = Flask(__name__)
	app.config.from_object('config')  # 载入config.py配置文件
	register_blueprint(app)
	return app


def register_blueprint(app):
	from app.web.book import web
	from app.web.hello import web
	app.register_blueprint(web)

