from . import web


@web.route("/hello")
def hello():
	header = {
		'content-type': 'text/plain', # 告诉浏览器怎么解析返回的文本
		# 'location': 'http://www.baidu.com' # 重定向
	}
	#  返回（信息，状态码，头文件）
	return "hello world", 200, header
