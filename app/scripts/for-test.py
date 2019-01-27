# websites={'myegy.cc':d.websites['myegy.cc']}
#, {'egybest':d.websites['egybest']}
d = Download()
data = d.search('for richer for poorer')
for name, val in data.items():
	print(name, val)
	print('\t', val['search_text'])
	print('\t', val['film_url'])

# link = 'https://search.yahoo.com/search?p=last+tango+in+paris'
# link = 'https://search.yahoo.com/search?p=wonder'
# s = Scraper()
# s.get(link)

# external_links = s.regex(r'http[s]*://[-/\.\w]+')
# internal_links = s.regex(r'href="(/[-/\.\w]+)"')

#soup = s.html_soup()

web = Yahoo()


films = [
	'2012',
	'sex tape',
	'space dogs', 
	'wonder', 
	'last tango in paris', 
	'Identitiy', 
	'fight club', 
	'3 idiots',
	'dangal',
	'pk',
	'ice age',
	'cam',
	'once upon a time',
	'who am i'
	'اسف علي الازعاج',
	'الكيف',
]



# for filmName in films:
# 	print(filmName)
# 	print('---------')
# 	yahoo = (web.yahoo(filmName))
# 	for key, val in yahoo.items():
# 		print('%s: %s' % (key, val))

# 	print()
# 	print()

# imdb = IMDB()

# for film in films:
# 	print(film)
# 	dta = imdb.imdb(film)
# 	if dta:
# 		for key, val in dta.items():
# 			if key == 'cast':
# 				for elm in val:
# 					for k, v in elm.items():
# 						print('\t%s: %s' % (k, v))
# 			else:
# 				print('%s: %s' % (key, val))

# 	print()
# 	print()

#imdb = web.imdb(link)

# print(convert_length('2h 13m 12s', 'h'))





'''
acrape any img
  always img which in <a>
  lead to page contain this bigger

  always main img bigger than all imgs in page
'''
