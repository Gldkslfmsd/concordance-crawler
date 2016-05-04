#!/usr/bin/env python3

'''Functions for crawling links from Bing Search.'''

import logging
import datetime
import requests

from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.core.parsing import parse
import ConcordanceCrawler.core.urlrequest as urlrequest
import six
if six.PY3:
	def encode(a):
		return a
else:
	def encode(a):
		return a.encode('utf-8')


class SERPError(Exception):
	def __init__(self, e=None):
		self.e = e

def crawl_links(target_word, bazword_gen = None):
	'''Crawls links from Bing Search. Uses bazword generator to get
	more keywords and therefore more pages with the target_word.

	Args:
		target_word
		number of pages with concordances, if not given, 1 is default
		bazword_gen -- bazword generator, if not given, RandomShortWords is used
	
	Returns:
		list of links, where a link is a string
			
	raises:
		SERPEror
	'''
	bazgen = bazword_gen if bazword_gen else RandomShortWords()

	keyword = bazgen.get_bazword() + " " + target_word
	links = [l['link'] for l in crawl_one_keyword(keyword)]

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
	
def crawl_one_keyword(keyword):
	'''Scrapes one keyword.

	Returns:
		list of links, a link is a dictionary with keys:
			link, rank, snippet, title, visible_link, date, keyword
			
	raises: SERPError
	'''
	url = get_keyword_url(keyword)
	logging.debug("trying to download SERP {}".format(url))
	try:
		rawhtml, headers = urlrequest.get_raw_html(url)
	except requests.exceptions.RequestException as e:
		raise SERPError(e)

	date = _date()

	if is_blocked(rawhtml):
		raise SERPError()

	#links = parse(rawhtml) + [{'link':"http://lesbartavelles13.free.fr/IMAGE-ISO/ENGLISH6EME.iso"}]

	links = parse(rawhtml)

	# adding scraping information to links
	for i in links:
		i['date'] = date
		i['keyword'] = keyword
		i['link'] = encode(i['link'])   #.encode('UTF-8')

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
	return 'Omluvte p' in rawhtml

def _date():
	'''Returns a string with current date.'''
	return str(datetime.datetime.now())







def filter_link_by_format(link):
	'''returns True/False
	if True, link is accepted and can be visited
	otherwise rejected
	
	it rejects links of non-text documents (hopefully)
	'''
	if any(link.lower().endswith(suffix) for suffix in [
		'.docx', '.doc', '.pdf', '.ppt', '.pptx', '.odt', '.img', '.iso']):
		return False
	return True

	

if __name__ == "__main__":
	res = crawl_links("core",number = 10)
	import pprint
	print(pprint.pformat(res))
