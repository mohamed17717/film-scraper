#!/usr/bin/env	python3

from requests import Session
from urllib.parse import unquote as decode_url
from bs4 import BeautifulSoup
from re import findall, search, match
from string import ascii_lowercase as ELetters
import threading
from time import sleep, time
import json 

class Scraper:
	"""
	docstring for Scraper
		this is some fucntions used mostly when scraping
	"""
	def __init__(self):
		super(Scraper, self).__init__()
		self.__setup()

		## args will be submit latter
		self.src = None

	def __setup(self):
		self.session = Session()
		self.session.headers.update({
			## very common user_agent
			'User_agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
		})

	def get(self, link):
		r = self.session.get(link) # , timeout= 3
		if r.status_code == 200:
			self.src = r.text 
		return self.src

	def html_soup(self):
		if self.src:
			return BeautifulSoup(self.src, 'html.parser')
		return BeautifulSoup('', 'html.parser')

class ScrapeWebsite:
	"""
	docstring for ScrapeWebsite
		this is some of functions each can 
		scrape specific data from specific website

		Websites List:
			- search.yahoo.com/search?p=last+tango+in+paris
			- imdb.com

			- wikipedia.org
			- allmovie.com
			- rottentomatoes.com
			- yts.am
			- elcinema.com
	"""
	def __init__(self):
		super(ScrapeWebsite, self).__init__()
		self.domains = ['wikipedia', 'imdb', 'rottentomatoes']
	
	def shift(self, lst):
		x = lst[0]
		lst.remove(x)
		return x

	def get_host(self, url):

		return url.split('//')[-1].split('/', 1)[0]

	def get_domain(self, host):
		
		return host.split('.')[-2]

	def defined_website(self, link):
		
		return self.domain(self.host(link)).lower() in self.domains

	def convert_length(self, length, to='m'):
		## lenght must be 15h 13m
		convert_map = {
			's':{'h': '*60*60 +', 'm': '*60 +', 's': '*1 +'},
			'm':{'h': '*60 +'   , 'm': '*1 +' , 's': '/60 +'},
			'h':{'h': '*1 +'    , 'm': '/60 +', 's': '/(60*60) +'},
		}
		my_map = convert_map[to]
		for unit, equivelant in my_map.items():
			length = length.replace(unit, equivelant)
		
		length = length.rstrip('+')

		try:
			return str(eval(length)) + to
		except:
			return False

	def englishName(self, filmName):
		
		return filmName[0].lower() in ELetters


	def get_soup(self, link):
		scraper = Scraper()
		scraper.get(link)
		return scraper.html_soup()

class Wikipedia(ScrapeWebsite):
	"""docstring for Wikipedia"""
	def __init__(self, arg):
		super(Wikipedia, self).__init__()
		self.arg = arg
		

	def external_sites(self):
		pass

	## Wikipedia
	def wikipedia(self, link):
		## get data and soup it
		soup = self.get_soup(link)

		return {
			'sites': self.external_sites(),
		}

class IMDB(ScrapeWebsite):
	"""docstring for IMDB"""
	def __init__(self):
		super(IMDB, self).__init__()
		self.soup = None
		
	def name(self):
		n = self.soup.select_one('meta[property="og:title"]')
		n = n['content']
		## ptrn  "name (year)"
		## so i only remove and join with '(' cus name may contain () itself
		return '('.join(n.split('(')[:-1]).strip()

	def year(self):
		txt = self.soup.title.text
		find = findall(r'\((.+)\)',txt)
		return find and find[-1]

	def mpaa(self):
		txt = self.soup.select_one('.subtext').text.lstrip()
		ptrn = r'[A-Z]+[-\dA-Z]*'
		find = match(ptrn, txt)
		return find and find.group()

	def length(self):
		elm = self.soup.select_one('div.title_wrapper .subtext')
		return elm.time.text.strip()

	def trailer(self):
		a = self.soup.select_one('div.slate_wrapper .slate a')
		link = a and  'https://imdb.com' + a['href'] or ''
		video_src, img_src = '', ''
		if link:
			img_src = a.img.get('src') or ''
			s = Scraper()
			src = s.get(link)
			video_src = search(r'"videoUrl":"(.+?)"', src)
			video_src = video_src and video_src.group(1).replace('\\u002F', '/') or ''
		return  {
			'video_src': video_src,
			'link': link,
			'img_src': img_src
		}

	def poster(self):
		img = self.soup.select_one('div.poster').img
		return img['src']

	def category(self):
		a = self.soup.select('div.title_wrapper .subtext a')
		return [i.text for i in a][:-1]

	def rating(self):
		elm = self.soup.select_one('div.imdbRating .ratingValue strong')
		txt = elm['title']

		rating, count = findall(r'[,\.\d]+', txt)

		return {'rating': rating, 'count': count}

	def brief(self):
		txt = self.soup.select_one('.plot_summary_wrapper .plot_summary .summary_text').text.strip()
		return txt

	def country(self):
		elms = self.soup.select('div#titleDetails .txt-block')
		txts = [i.text.lower().split() for i in elms]
		for txt in txts:
			if 'country' in txt[0]:
				return [i for i in txt[1:] if match(r'\w+', i)]
		
	def language(self):
		elms = self.soup.select('div#titleDetails .txt-block')
		txts = [i.text.lower().split() for i in elms]
		for txt in txts:
			if 'language' in txt[0]:
				return [i for i in txt[1:] if match(r'\w+', i)]

	def cast(self):
		rows = self.soup.select('.cast_list tr')
		data = ()

		for row in rows[1:]:
			## clms are tds
			clms = row.select('td')
			if len(clms) != 4:
				continue
			photo, name, _, chracter = clms
			## made data in list cus i care with order
			data += ({
				'name': name.text.strip(),
				'imdb_link': name.a and 'imdb.com'+name.a['href'] or '',
				'chracter': ' '.join(chracter.text.split()),
				'photo': photo.img.get('loadlate') or photo.img['src']
			},)

		return data

	def reviews(self):
		pass 
	def prizes_won(self):
		pass
	def prizes_nomenee(self):
		pass 

	def awards(self):
		link = link + '/awards'
		pass 		

	def search(self, filmName):
		link = 'https://www.imdb.com/find?q=%s&s=tt'
		link = link % filmName.lower().replace(' ', '+')

		## scrape src
		soup = self.get_soup(link)

		anchor = soup.select_one('table.findList tr.findResult a')
		# path   = '/'.join(anchor['href'].split('/')[:-1])
		path = anchor and anchor['href']
		return path and 'https://www.imdb.com' + path or None

	## return IMDB all possible data
	def imdb(self, filmName=None, link=None):
		link = link or self.search(filmName)
		if not link:
			return None

		## get data and soup it
		self.soup = self.get_soup(link)
		## find data
		return {
			'name'    : self.name(),
			'year'    : self.year(),
			'mpaa'    : self.mpaa(),
			'length'  : self.length(),
			'trailer' : self.trailer(),
			'poster'  : self.poster(),
			'category': self.category(),
			'rating'  : {'imdb': self.rating()},
			'brief_en': self.brief(),
			'country' : self.country(),
			'language': self.language(),
			'cast'    : self.cast(),

			# 'reviews' : self.reviews(),
			# 'prizes-won': self.prizes_won(),
			# 'prizes-nomenee': self.prizes_nomenee(),
		}

class Yahoo(ScrapeWebsite):
	"""docstring for Yahoo
		scrape from yahoo accroding to its structure
	"""
	def __init__(self):
		super(Yahoo, self).__init__()
		## general area of data
		self.soup = None

	def extract_redirect_link_yahoo(self, link):
		## check its yahoo
		host = self.get_host(link)
		if 'yahoo' in host:
			## start with 'r' this is redirect else skip it
			if 'r' == host.split('.', 1)[0]:
				## this is regular vars in link
				link = decode_url(link.split('/RK=', 1)[0].split('RU=', 1)[-1])

		return link

	## start functions only for right area ##
	def trailer(self):
		iframe = self.soup.iframe
		return iframe and iframe['data-src'] or None

	def name(self):
		## first p always contain name
		return self.soup.select_one('div.compImageProfile p').text

	def mpaa(self):
		## mpaa always first span in second p or its not exist
		spans = self.soup.select_one('div.compImageProfile').select('p:nth-of-type(2) span')
		return len(spans) == 2 and spans[0].text or None

	def year(self):
		## year - type - length
		spanText = self.soup.select_one('div.compImageProfile').select('p:nth-of-type(2) span')[-1].text
		ptrn = r'\d\d\d\d'
		matchedData = search(ptrn, spanText)
		return  matchedData and matchedData.group() or None

	def category(self):
		spanText = self.soup.select_one('div.compImageProfile').select('p:nth-of-type(2) span')[-1].text
		ptrn = r'[A-Z][a-z]+'
		matchedData = search(ptrn, spanText)
		return  matchedData and matchedData.group() or None

	def length(self):
		spanText = self.soup.select_one('div.compImageProfile').select('p:nth-of-type(2) span')[-1].text
		ptrn = r'\dh [12345]{0,1}[0-9]m'
		matchedData = search(ptrn, spanText)
		return  matchedData and matchedData.group() or None

	def poster(self):
		a = self.soup.select_one('div.compImageProfile').a
		return a and a['href']

	def brief(self):
		textElms = self.soup.select('div.compText > p')
		## brief must be longest text
		mx = 0
		brief = ''
		for elm in textElms:
			l = len(elm.text)
			if l > mx and elm.a:
				elm.a.replaceWith('')
				brief = elm.text.rstrip()
				mx    = l
		return brief

	def sites(self):
		## contain links to wiki imdb rotten-tomato		
		ulElms = self.soup.select('ul')
		sites  = {}
		## i wanna last ul
		ulElm_a = self.soup.select('ul:nth-of-type(%i) li a[title]' % len(ulElms))
		[sites.update({
				a['title'].lower(): self.extract_redirect_link_yahoo(a['href'])
			}) for a in ulElm_a]

		return sites

	## End functions only for right area ##

	## start Left Area ##
	def leftAreaData(self):
		## list elms in left side
		left_li = self.soup

		sites = {}
		for li in left_li:
			## link and title all in a elm
			a = li.h3.a
			title = (a and a.text) or ''
			link = (a and a['href']) or ''
			if link:
				link   = self.extract_redirect_link_yahoo(link)
				host   = self.get_host(link)
				domain = self.get_domain(host).lower()
				if domain in self.domains:
					sites.update({domain: {'title': title, 'link': link}})
		return sites
	## End Left Area ##


	## return Yahoo all possible data
	def yahoo(self, filmName):
		## link
		link = 'https://search.yahoo.com/search?p=%s'
		link = link % filmName.lower().replace(' ', '+')

		## get data and soup it
		soup = self.get_soup(link)


		## find data
		right = soup.select_one('div#right div')
		## right might be exist but not refering to my movie
		## movies always have year also it may be a series
		right_text = right and right.text.lower() or ''
		first_cmponent_text = right and right.select_one('div.compImageProfile').text or ''
		is_years_in_text = bool(  search(r'(19[5-9][0-9]|20[01][0-9])', first_cmponent_text)  )

		is_valid = is_years_in_text or ('imdb' in right_text) or ('created by' in right_text)
		if is_valid:
			self.soup = right

			return {
				'trailer': self.trailer(),
				'name': self.name(),
				'mpaa': self.mpaa(),
				'year': self.year(),
				'category': self.category(),
				'length': self.length(),
				'poster': self.poster(),
				'brief_en': self.brief(),
				'sites': self.sites()
			}
		else:
			## yahoo may not detect this as a movie from first
			## so search again and add movie at the end if u not added it before
			if (not filmName.endswith('movie')) and self.englishName(filmName):
				return self.yahoo('%s movie' % filmName)

			## if u dont find in the right side
			## start see if there is useful data in left
			self.soup  = soup.select('div#left div#main div#web > ol > li')
			
			return {'extra-sites': self.leftAreaData()}

class Download(ScrapeWebsite):
	"""docstring for Download"""
	def __init__(self, FilmInformation):
		super(Download, self).__init__()

		self.FilmInformation = FilmInformation
		self.data = {}
		import os
		os.system('pwd')
		with open('app/scripts/scrapped-websites.json') as f:
			self.websites = json.loads(f.read())

	def clean_spaces(self, text):
		''' remove tabs and lines and many spaces replace all with one space '''
		return ' '.join( findall(r'\S+',text) )

	def match_year(self, text):
		## match 1950 to 1999
		## match 2000 to 2019
		year_ptrn= r'(19[5-9][0-9]|20[01][0-9])'
		
		found = search(year_ptrn, text)
		found = found and found.group()

		film_year = str(self.FilmInformation['year'])
		return found and found == film_year

	def match_name(self, text):
		ptrn = r'\w+'
		film_name = findall(ptrn, self.FilmInformation['name'].lower())
		matches = findall(ptrn, text.lower())
		for word in film_name:
			if not word in matches:
				return False
		return True

	def clean_not_matched(self, results):
		cleaned = ()
		for result in results :
			txt = result.text
			is_year = self.match_year(txt)
			is_name = self.match_name(txt)
			if is_name:
				if is_year or is_year == None:
					cleaned += (result, )
		return cleaned

	def __searchHelper__(self, name, site):
		## build search url
		query = ' '.join([self.FilmInformation[i] for i in site['search']['search_query']])
		search_url = site['url'] + site['search']['link'] % query
		## scrape it
		soup = self.get_soup(search_url)
		## get search results
		results = soup.select( site['search']['selector'] )
		## clean the results get matched
		results = self.clean_not_matched(results)

		if results:
			## extract url and text
			urls = []
			txts = []
			for elm in results:
				# txts.append(elm.text)
				txts.append( self.clean_spaces( elm.text ) )
				if elm.name != 'a':
					elm = elm.a
				url = elm.get('href') or ''
				url = (url.startswith('/') and site['url'] + url) or url
				urls.append( url )

			## update my data
			site['search']['return'].update({
				'film_url': urls,
				'search_text': txts,
				'zipped': list(zip(urls, txts))
			})
			self.data[name] = site['search']['return']

	def search(self,websites=None):
		# filmName = self.FilmInformation.get('user-query')
		## can't put default using self
		websites = websites or self.websites
		for name, site in websites.items():
			thread = threading.Thread(target=self.__searchHelper__, args=(name, site))
			# thread.daemon = 1
			# thread.setName(name)
			thread.start()
		loop = 0
		while (len(threading.enumerate()) > 1) and (len(self.data) < 5):
			print(loop,len(threading.enumerate()), len(self.data))
			if loop >= 10: break
			sleep(0.5)
			loop += 1


		return self.data


class Film:
	"""
		docstring for Film
			get all possible data about a film
	"""

	def __init__(self, filmName):
		super(Film, self).__init__()

		self.name = filmName
		self.info = {
			'user-query': self.name,
			## main data
			'name'    : None,
			'year'    : None,
			'mpaa'    : None,
			'length'  : None,
			'poster'  : None,
			'category': None,
			
			'rating'  : None,
			'trailer' : None,
			'brief_en': None,
			'brief_ar': None,
			## more data
			'country' : None,
			'language': None,
			'cast'    : None,
			'reviews' : None,

			'prizes_won': None,
			'prizes_nomenee': None,
			## download
			'torrent' : None,
			'download': None,
			'subtitle': None,
		}

	def information(self):
		'''search in yahoo, imdb, other possibles'''
		imdb  = IMDB()
		yahoo = Yahoo()


		yahoo_data = yahoo.yahoo(self.name)
		## try if data got from right area (trusted) do somthing
		## except doing somthng else
		try:
			sites = yahoo_data.pop('sites')
			self.info.update(yahoo_data)

			imdb_url = sites.get('imdb')
		except KeyError as e:
			#imdb_url = yahoo_data[ 'extra-sites' ].get('imdb')['link']
			imdb_url = None
			pass
		imdb_data = (imdb_url and imdb.imdb(link = imdb_url)) or imdb.imdb(filmName= self.name)
		self.info.update(imdb_data)

	def download_w(self):
		'''
			get download data from websites (arabic sites with subtitle etc)
		'''

		## filter depend on self.info
		download = Download( self.info )
		data = download.search()
		self.info['download'] = data

	def build(self):
		self.information()
		self.download_w()

		return self.info


# if __name__ == '__main__':
# 	filmName = 'fight club'
# 	film = Film(filmName)
# 	film.build()
# 	from pprint import pprint
# 	pprint(film.info)

# f = Film('aquaman')
# f.build()
# info = f.info
# download = info.pop('download')

# for k,v in info.items():
# 	print(k, ': ',  v)

# for k,v in download.items():
# 	print(k, '\n\t' , v['film_url'])

# from json import dumps
# filmName = 'identity'
# f = Film(filmName)
# f.build()
# info = f.info
# print(dumps(info))


# 'rating'  : None,
# 'download': None,

# 'reviews' : None,
# 'prizes-won': None,
# 'prizes-nomenee': None,
# 'torrent' : None,
# 'subtitle': None,

## https://www.totaleclips.com/Player/Bounce.aspx?eclipid=e17963&bitrateid=455&vendorid=102&type=.mp4