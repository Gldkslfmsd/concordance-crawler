#!/usr/bin/env python3

# This will be a main file of Concordance Crawler. 

from multiprocessing import Pool
import requests
import datetime

from bazwords import *
import parse


class ConcordanceCrawler():
# TODO: set bazword generators
#		bazword_gen = None,
#		bazwords = None
	def crawl(self, target_word, number = 100):
		'''Crawls concordances.

		Args:
			target_word
			number of pages with concordances
		
		Returns:
			list of links, where a link is a dictionary
		'''
		bazgen = RandomShortWords()
		links = []
		for i in range(number):
			keyword = bazgen.get_bazword() + " " + target_word
			bingresult = self.crawlonekeyword(keyword)
#			pageresult = self.visitpage(bingresult)
			links.extend(bingresult)
			
		return links

	# TODO: make it same
	def crawl_concurrent(self,bazwords, word, processes=10):
		"""Same as crawl, but does it concurrently and faster.
		"""
		pool = Pool(processes)
		bazwords = map(lambda i: i + " " + word, bazwords)
		result = pool.map(crawlonekeyword, bazwords)
		return result

	def get_keyword_url(self,keyword):
		replacedspaces = keyword.replace(" ","+")
		# 59 links on page is maximum, then it blocks (probably)
		url = "http://www.bing.com/search?q={keyword}&first=1&count=59&FORM=PERE1".format(
			keyword = replacedspaces
		)
		return url
		
	def crawlonekeyword(self,keyword):
		'''Scrapes one keyword.

		Returns:
			list of links, a link is a dictionary with keys:
			TODO
		'''
		url = self.get_keyword_url(keyword)
		rawhtml = requests.get(url).text

		date = ConcordanceCrawler.__date()

		if self.is_blocked(rawhtml):
			# TODO really just return None?
			return None

		# adding scraping information to links
		links = parse.parseBing(rawhtml)
		for i in links:
			i['date'] = date
			i['keyword'] = keyword

		return links

	def is_blocked(self,rawhtml):
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

	def visitpage(self,bingresult):
		'''Visits page and tries to find a concordance'''
		# TODO
		return bingresult


	def __date():
		'''Returns a string with current date.'''
		return str(datetime.datetime.now())





	

if __name__ == "__main__":
	cc = ConcordanceCrawler()
	res = cc.crawl("write",number = 10)
	import pprint
	print(pprint.pformat(res))
