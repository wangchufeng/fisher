from flask import Flask
from helper import is_isbn_or_key

app = Flask(__name__)
app.config.from_object('config')  # 载入config.py配置文件

@app.route("/hello")
def hello():
	header = {
		'content-type': 'text/plain', # 告诉浏览器怎么解析返回的文本
		# 'location': 'http://www.baidu.com' # 重定向
	}
	#  返回（信息，状态码，头文件）
	return "hello world", 200, header


@app.route('book/search/<q>/<page>')
def search(q,page):
	isbn_or_key = is_isbn_or_key(q)
## 准备开始调用api


if __name__ == "__main__":
	#  在生产环境下使用 nginx + uwsgi 来配置
	#  uwsgi会加载这个入口文件
	#  若没有写 if __name__ == "__main__":
	#  则下面语句又会被执行，又会启动flask自带的服务器
	app.run(host='0.0.0.0', debug = app.config['DEBUG'], port=5000)
