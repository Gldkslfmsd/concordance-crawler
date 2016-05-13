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

import stopit

class VisitTooLongException(Exception):
	'''Visit took too long'''

class Visitor():
	attributes = ['get_raw_html', 'get_visible_text', 'predict_format',
		'accept_format', 'sentence_segmentation',
		'language_filter', 'norm_encoding', 'concordance_filtering',
		'sentence_filter']

	def __init__(self):
		self.get_raw_html = urlrequest.get_raw_html
		self.get_visible_text = VisibleTextParser().get_visible_text
		self.predict_format = FormatPredictor().predict_format
		self.accept_format = FormatFilter().accept_format
		self.sentence_segmentation = segmenter.sentence_segmentation
		self.language_filter = EngDetector().is_english
		self.norm_encoding = encoding.norm_encoding
		self.concordance_filtering = concordance_filtering
		self.sentence_filter = lambda _: True  # default sentence filter does nothing

#		open("logfile","w").close()
		#self.i = 0
	
	def visit(self, url, targets):
		'''Visits a page on given url and extracts all sentences containing
		target word from visible text.
	
		Args:
			url
			targets -- a list of target words
	
		Returns:
			a list of quadruples (concordance, target_word, start, end) or None
			e.g.
			>>> visit('https://someurl.com', ['hi', 'hello'])
			[('Hi!', 'hi', 0, 2), ('Hello there!', 'hello', 0, 4)]

			>>> visit('http://nonenglishsite.cz/', ['hoovercraft'])
			None  # returns None if the text e.g. doesn't pass language filter
			'''
		raw_data, headers = self.get_raw_html(url)

		data_format = self.predict_format(raw_data)
		if not self.accept_format(data_format):
		  return None

		normed_data = self.norm_encoding(raw_data, headers)
		 
		del raw_data
		del headers
		if not normed_data:
			return None

		text = self.get_visible_text(normed_data)

		# saving texts for language filter accuracy test
		#with open(targets[0] + str(self.i), "w") as f:
		#	f.write(text)
		#with open(targets[0] + str(self.i) + ".html", "w") as f:
		#  	f.write(raw_data)
		#self.i += 1
		  
		del normed_data
		if not self.language_filter(text):
			return None

		# logging charset in http header and in meta tag 
#		m = re.search(r"charset=\S*", raw_data)
#		if m:
#			x = m.string[m.start():m.end()]
#			x = re.sub(r"['\"]","",x)
#			x = re.sub(r"charset=","",x)
#			x = re.sub(r"[</>].*",r"",x)
#		else:
#			x = ""
#		m = re.search(r"charset=\S*",raw_data)
#		self.i += 1
#		f=open("logfile","a")
#		f.write(targets[0]+str(self.i)+"; header:"+ headers['Content-Type']+"; metatag:"+x+"\n")
#		f.close()


		sentences = filter(self.sentence_filter,
			self.sentence_segmentation(text))

		concordances = []
		for s in sentences:
			t = self.concordance_filtering(s, targets)
			if t:
				target, start, end = t
				concordances.append((s, target, start, end))
		return concordances

	def concordances_from_link(self, link, targets):
		'''Gets list of links, visits them and crawls concordances.
		
		Args:
			link
			targets

		Returns:
			list of concordances, where a concordance is a dict with keys:
				url, date, concordance (a sentence), keyword etc.
		'''
		url = link

		with stopit.ThreadingTimeout(60) as timeout:
			concs = self.visit(url,targets)

		if timeout.state != stopit.ThreadingTimeout.EXECUTED:
			raise VisitTooLongException()

		if concs is None:
			return []
		concordances = []
		date = str(datetime.datetime.now())
		for con, target, start, end in concs:
			c = {
				'url':url,
				'date':date,
				'concordance':con,
				'keyword':target,
				'start': start,
				'end': end,
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
	print(v.visit("https://en.wikipedia.org/wiki/Viceroy_of_Liangguang",["of"]))

	try:
		print(v.visit("http://cgg.mff.cuni.cz/~pepca/lectures/cv/083/083DominikMachacek.avi",["SDSDFSFSDFS"]))
	except ValueError as e:
		print(e)
	#print(v.visit("http://lesbartavelles13.free.fr/IMAGE-ISO/ENGLISH6EME.iso", ["SDFS"]))
