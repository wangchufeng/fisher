def is_isbn_or_key(word):
	"""
			判断 word 是关键字 还是ISBN
			isbn 13个0到9的数字组成， 或者10个加一些 ‘-’
		"""
	# isdigit() 判断字符串是否全为数字
	isbn_or_key = "key"
	if len(word) == 13 and word.isdigit():
		isbn_or_key = "isbn"
	short_word = word.replace('-','')
	if '-' in word and len(short_word) == 10 and short_word.isdigit():
		isbn_or_key = "isbn"
	return isbn_or_key
