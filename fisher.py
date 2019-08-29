from app import create_app

app = create_app()

if __name__ == "__main__":
	#  在生产环境下使用 nginx + uwsgi 来配置
	#  uwsgi会加载这个入口文件
	#  若没有写 if __name__ == "__main__":
	#  则下面语句又会被执行，又会启动flask自带的服务器
	#
	# 启动flask自带的服务器（webserver），其他的webserver有nginx apache

	#  FLASK的debug和 pycharm的debug都开的话，代码会执行两次
	app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5000)
