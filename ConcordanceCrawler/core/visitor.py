#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Visit given url and find there a concordance.'''

import re
import datetime

from ConcordanceCrawler.core.visible_text import *
from ConcordanceCrawler.core.simple_concordance_filter import regex_concordance_filtering as concordance_filtering
import ConcordanceCrawler.core.segmenter as segmenter
import ConcordanceCrawler.core.urlrequest as urlrequest
import ConcordanceCrawler.core.encoding as encoding

from ConcordanceCrawler.core.eng_detect.eng_detect import EngDetector

class Visitor():
	attributes = ['get_raw_html', 'get_visible_text', 'predict_format',
		'accept_format', 'sentence_segmentation',
		'language_filter', 'norm_encoding', 'concordance_filtering']

	def __init__(self):
		self.get_raw_html = urlrequest.get_raw_html
		self.get_visible_text = VisibleTextParser().get_visible_text
		self.predict_format = FormatPredictor().predict_format
		self.accept_format = FormatFilter().accept_format
		self.sentence_segmentation = segmenter.sentence_segmentation
		self.language_filter = EngDetector().is_english
		self.norm_encoding = encoding.norm_encoding
		self.concordance_filtering = concordance_filtering
	
	def visit(self, url, targets):
		'''Visits a page on given url and extracts all sentences containing
		target word from visible text.
	
		Args:
			url
			targets -- a list of target words
	
		Returns:
			a list of pairs (concordance, target_word) or None
			e.g.
			>>> visit('https://someurl.com', ['hi', 'hello'])
			[('Hi!', 'hi'), ('Hello there!', 'hello')]

			>>> visit('http://nonenglishsite.cz/', ['hoovercraft'])
			None  # returns None if the text e.g. doesn't pass language filter
			'''
		# TODO: rename it and add returning header
		raw_data, header = self.get_raw_html(url), None
		normed_data = self.norm_encoding(raw_data, header)
		data_format = self.predict_format(normed_data)
		if not self.accept_format(data_format):
			return None
		text = self.get_visible_text(normed_data)

		if not self.language_filter(text):
			return None

		sentences = self.sentence_segmentation(text)

		concordances = []
		for s in sentences:
			t = self.concordance_filtering(s, targets)
			if t:
				concordances.append((s,t))
		return concordances

	def concordances_from_link(self, link, target_words):
		'''Gets list of links, visits them and crawls concordances.
		
		Args:
			links -- list of dicts, where dict is a link and has at least key 'link'
			target_words

		Returns:
			list of concordances, where a concordance is a dict with keys:
				url, date, concordance (a sentence), keyword
		'''
		url = link['link']
		concs = self.visit(url,target_words)
		if concs is None:
			return []
		concordances = []
		date = str(datetime.datetime.now())
		for con, target in concs:
			c = {
				'url':url,
				'date':date,
				'concordance':con,
				'keyword':target,
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
