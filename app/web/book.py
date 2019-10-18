from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web
import json
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
	books = BookCollection()

	if form.validate():
		# strip函数剔除字符串前后空格
		q = form.q.data.strip()
		page = form.page.data
		isbn_or_key = is_isbn_or_key(q)
		yushu_book = YuShuBook()

		if isbn_or_key == 'isbn':
			yushu_book.search_by_isbn(q)
		else:
			yushu_book.search_by_keyword(q, page)
		books.fill(yushu_book, q)
		#  return json.dumps(result), 200, {'content-type': 'appplication/json'}

		#  返回的result是一个字典,需要将其序列化，python无法直接序列化一个对象
		#  所以return jsonify(books)时候，books里面含有对象，会报错解决办法如下，利用__dict__属性

		# return json.dumps(books, default=lambda o: o.__dict__)

	else:
		flash('搜索的关键字不符合要求，请重新输入关键字')
		# return jsonify(form.errors)
	return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
	has_in_gift = False
	has_in_wish = False

	#  取数据详情数据
	yushu_book = YuShuBook()
	yushu_book.search_by_isbn(isbn)
	book = BookViewModel(yushu_book.first)

	if current_user.is_authenticated:
		if Gift.query.filter_by(uid=current_user.id, isbn=isbn
				, launched=False).first():
			has_in_gift = True
		if Wish.query.filter_by(uid=current_user.id, isbn=isbn
				, launched=False).first():
			has_in_wish = True

	trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
	trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

	trade_gifts_model = TradeInfo(trade_gifts)
	trade_gifts_wishes = TradeInfo(trade_wishes)

	return render_template('book_detail.html', book=book, wishes=trade_gifts_wishes, gifts=trade_gifts_model, has_in_gift=has_in_gift, has_in_wish=has_in_wish)



