#!/usr/bin/env python3

'''Visit given url and find there a concordance.'''

import re
import datetime

from ConcordanceCrawler.core.visible_text import *
from ConcordanceCrawler.core.internet_user import InternetUser
import ConcordanceCrawler.core.segmenter

class Visitor(InternetUser):
	get_visible_text = VisibleTextParser().get_visible_text
	predict_format = FormatPredictor().predict_format
	accept_format = FormatFilter().accept_format
	sentence_segmentation = segmenter.sentence_segmentation
	
	def visit(self, url, target):
		'''Visits a page on given url and extracts all sentences containing
		target word from visible text.
	
		Args:
			url
			target
	
		Returns:
			a list of sentences
		'''
		raw_data = self.get_raw_html(url)
		data_format = self.predict_format(raw_data)
		if not self.accept_format(data_format):
			return None
		text = self.get_visible_text(raw_data)

		sentences = self.sentence_segmentation(text)
	
		concordances = list(filter(ConcordanceFilter(target).process, sentences))
	
		return concordances

	def visit_links(self, links, target_word):
		'''Gets list of links, visits them and crawls concordances.
		
		Args:
			links -- list of dicts, where dict is a link and has at least key 'link'
			target_word

		Returns:
			list of concordances, where a concordance is a dict with keys:
				url, date, concordance (a sentence), keyword
		'''
		concordances = []
		for i in links:
			url = i['link']
			concs = visit(url,target_word)
			date = str(datetime.datetime.now())
			for j in concs:
				c = {
					'url':url,
					'date':date,
					'concordance':j,
					'keyword':target_word
				}
				concordances.append(c)

		return concordances

if __name__ == "__main__":
#	pairs = [("http://leapfroggroup.org/","group"),
#		("http://www.thinkbabynames.com/meaning/1/Dominik","Dominik"),
#		("https://hungryhouse.co.uk/indian-takeaway","takeaway"),
#		("http://www.writeawriting.com/","write")]

#	for url,target in pairs:
#		print()
#		print()
#		print(url,target)
#		print("==========================")
#		con = visit(url,target)
#		for i in con:
#			# to better see ends of lines
#			print(">>>"+i+"<<<")

	import requests
	v = Visitor()
	print(v.visit("https://en.wikipedia.org/wiki/Viceroy_of_Liangguang","of"))
