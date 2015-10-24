#!/usr/bin/env python3

'''Functions for crawling links from Bing Search.'''

import logging
import datetime

from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.core.parsing import parse
import ConcordanceCrawler.core.urlrequest as urlrequest

def crawl_links(target_word, number = 1, bazword_gen = None):
	'''Crawls links from Bing Search. Uses bazword generator to get
	more keywords and therefore more pages with the target_word.

	Args:
		target_word
		number of pages with concordances, if not given, 1 is default
		bazword_gen -- bazword generator, if not given, RandomShortWords is used
	
	Returns:
		list of links, where a link is a dictionary containing keys 
			link, rank, snippet, title, visible_link, date, keyword
	'''
	bazgen = bazword_gen if bazword_gen else RandomShortWords()
	links = []
	for i in range(number):
		keyword = bazgen.get_bazword() + " " + target_word
		bingresult = crawlonekeyword(keyword)
		links.extend(bingresult)
		
	return links

# 59 links on page is maximum, more is blocked (probably)
LINKS_PER_PAGE = 59

def get_keyword_url(keyword):
	'''Returns url of Bing Search where you can find links with keyword.'''
	replacedspaces = keyword.replace(" ","+")
	url = "http://www.bing.com/search?q={keyword}&first=1&count={number_of_links}&FORM=PERE1".format(
		keyword = replacedspaces,
		number_of_links = LINKS_PER_PAGE
	)
	return url
	
def crawlonekeyword(keyword):
	'''Scrapes one keyword.

	Returns:
		list of links, a link is a dictionary with keys:
			link, rank, snippet, title, visible_link, date, keyword
	'''
	url = get_keyword_url(keyword)
	logging.debug("trying to download SERP {}".format(url))
	rawhtml = urlrequest.get_raw_html(url)

	date = _date()

	if is_blocked(rawhtml):
		return None

	# adding scraping information to links
	links = parse(rawhtml)
	for i in links:
		i['date'] = date
		i['keyword'] = keyword

	return links

def is_blocked(rawhtml):
	'''This is quick and easy control of blocked file with captcha

	Returns:
		True if the query was blocked
		False otherwise
	'''
	# sometimes you get 115 bytes file with a strange code (e.g. if you try 30000
	# requests per minute)
	if len(rawhtml)<120:
		return True 
	# I can see this in Czech Republic, in other countries it may differ!
	return 'Omluvte přerušení' in rawhtml

def _date():
	'''Returns a string with current date.'''
	return str(datetime.datetime.now())




	

if __name__ == "__main__":
	res = crawl_links("core",number = 10)
	import pprint
	print(pprint.pformat(res))
