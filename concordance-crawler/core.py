#!/usr/bin/env python3

# This will be a main file of Concordance Crawler. 

import parse
from multiprocessing import Pool

def crawl(bazwords, word):
	'''Starts scraping with a set of keywords. A keyword is a particular
	bazword + word
	
	Args:
		bazwords -- list of bazwords
		word -- a concordance
	'''
	for i in bazwords:
		keyword = i + " " + word
#		print(keyword)
		print(crawlonekeyword(keyword))

def crawl_concurrent(bazwords, word, processes=10):
	"""Same as crawl, but does it concurrently and faster.
	"""
	pool = Pool(processes)
	bazwords = map(lambda i: i + " " + word, bazwords)
	result = pool.map(crawlonekeyword, bazwords)
	for i in result:
		print(i)
	
def crawlonekeyword(keyword):
	'''Scrapes one keyword.
	'''
	replacedspaces = keyword.replace(" ","+")
	url = "http://www.bing.com/search?q={keyword}&first=21&FORM=PERE1".format(
		keyword = replacedspaces
	)
	return keyword + "\n" + parse.parseBing(url)
	
import bazwords
baz = bazwords.RandomShortWords(0)
crawl_concurrent(
	[baz.get_bazword() for i in range(1000)],"browse")
