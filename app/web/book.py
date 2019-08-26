from flask import jsonify, request
from helper import is_isbn_or_key
from yushu_book import YuShuBook
from . import web
from app.forms.book import SearchForm
#  使用蓝图来注册视图函数 将多个视图拆分多个模块


# @web.route('/book/search/<q>/<page>')
# def search(q,page):  这样的路由格式是   /book/search/31234871029/1


@web.route('/book/search')
def search():
	# q = request.args['q']  #  /book/search?q=423423444&page=1
	# page = request.args['page']
	#  request.args下面还包含许多其他信息，但是是不可变字典
	#  a = request.args.to_dict()   将其转为可变字典
	form = SearchForm(request.args)
	if form.validate():
		q = form.q.data.strip()
		page = form.page.data
		isbn_or_key = is_isbn_or_key(q)
		if isbn_or_key == 'isbn':
			result = YuShuBook.search_by_isbn(q)
		else:
			result = YuShuBook.search_by_key(q)
		#  返回的result是一个字典,需要将其序列化
		#  return json.dumps(result), 200, {'content-type': 'appplication/json'}
		return jsonify(result)
	else:
		return jsonify({"msg": "参数校验失败"})
