#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Visit given url and find there a concordance.'''

import re
import datetime

from ConcordanceCrawler.core.visible_text import *
from ConcordanceCrawler.core.concordance_filter import concordance_filtering
import ConcordanceCrawler.core.segmenter as segmenter
import ConcordanceCrawler.core.language_analysis as language_analysis
import ConcordanceCrawler.core.urlrequest as urlrequest
import ConcordanceCrawler.core.encoding as encoding


class Visitor():
	attributes = ['get_raw_html', 'get_visible_text', 'predict_format',
		'accept_format', 'sentence_segmentation', 'predict_language',
		'accept_language', 'norm_encoding', 'concordance_filtering']

	def __init__(self):
		self.get_raw_html = urlrequest.get_raw_html
		self.get_visible_text = VisibleTextParser().get_visible_text
		self.predict_format = FormatPredictor().predict_format
		self.accept_format = FormatFilter().accept_format
		self.sentence_segmentation = segmenter.sentence_segmentation
		self.predict_language = language_analysis.predict_language
		self.accept_language = language_analysis.accept_language
		self.norm_encoding = encoding.norm_encoding
		self.concordance_filtering = concordance_filtering
	
	def visit(self, url, target):
		'''Visits a page on given url and extracts all sentences containing
		target word from visible text.
	
		Args:
			url
			target
	
		Returns:
			a list of sentences or None
		'''
		# TODO: rename it and add returning header
		raw_data, header = self.get_raw_html(url), None
		normed_data = self.norm_encoding(raw_data, header)
		data_format = self.predict_format(normed_data)
		if not self.accept_format(data_format):
			return None
		text = self.get_visible_text(normed_data)
		language = self.predict_language(text)
		if not self.accept_language(language):
			return None

		sentences = self.sentence_segmentation(text)
	
		concordances = list(filter(lambda s: self.concordance_filtering(target,s), sentences))
	
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
			concs = self.visit(url,target_word)
			if concs is None:
				continue
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
