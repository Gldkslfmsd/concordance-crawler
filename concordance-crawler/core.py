#!/usr/bin/env python3

# This will be a main file of Concordance Crawler. 

import parse
from multiprocessing import Pool
import requests

from bazwords import *

class ConcordanceCrawler():
# TODO: set bazword generators
#		bazword_gen = None,
#		bazwords = None
	def crawl_concordances(self, target_word, number = 100):
		'''Crawls concordances.

		Args:
			target_word
			number of pages with concordances
		
		Returns:
			TODO
		'''
		bazgen = RandomShortWords()
		for i in range(number):
			keyword = bazgen.get_bazword() + " " + target_word
			bingresult = self.crawlonekeyword(keyword)
			pageresult = self.visitpage(bingresult)
			print(pageresult)

	def crawl_concurrent(self,bazwords, word, processes=10):
		"""Same as crawl, but does it concurrently and faster.
		"""
		pool = Pool(processes)
		bazwords = map(lambda i: i + " " + word, bazwords)
		result = pool.map(crawlonekeyword, bazwords)
		return result
#	for i in result:
#		print(i)

	def get_keyword_url(self,keyword):
		replacedspaces = keyword.replace(" ","+")
		url = "http://www.bing.com/search?q={keyword}&first=1&FORM=PERE1".format(
			keyword = replacedspaces
		)
		return url
		
	def crawlonekeyword(self,keyword):
		'''Scrapes one keyword.
		'''
		url = self.get_keyword_url(keyword)
		rawhtml = requests.get(url).text
		# když je to zablokované:
		#if rawhtml[15414:15431] == 'Omluvte přerušení':
		#	pass

		return keyword + "\n" + parse.parseBing(rawhtml)

	def visitpage(self,bingresult):
		'''Visits page and tries to find a concordance'''
		# TODO
		return bingresult







	

if __name__ == "__main__":
	cc = ConcordanceCrawler()
	cc.crawl_concordances("dominik",number = 10)
