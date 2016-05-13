#!/usr/bin/env python3

"""Bazwords generators"""

import random

# this is an abstract base class
class AbstractBazwordGenerator(object):
  
	def get_bazword(self):
		'''returns a bazword on every call'''
		raise NotImplemented("override this in a descendant class")

class RandomShortWords(AbstractBazwordGenerator):
	"""Generates bazwords that look like 4 random letters"""
	# this is list of all letters
	letters = [ chr(a) for a in range(ord('a'),ord('z')+1) ]
	def __init__(self,seed = None):
		if seed:
			random.seed(seed)

	def get_bazword(self):
		baz = ""
		for i in range(4):
			baz += random.choice(self.letters)
		return baz

import ConcordanceCrawler.core.urlrequest as urlrequest
from bs4 import BeautifulSoup
class WikipediaRandomArticleTitles(AbstractBazwordGenerator):
	'''Scrapes random article from wikipedia and yields words from its title.'''
	
	def __init__(self):
		self._gen = self._generate()

	def _generate(self):
		while True:
			x,_ = urlrequest.get_raw_html('https://en.wikipedia.org/wiki/Special:Random')
			pagetitle = BeautifulSoup(x,"lxml").html.head.title.string
			# there is " - Wikipedia, the free encyclopedia" in the end of every
			# page title, I'm removing it
			title = pagetitle[:-len(" - Wikipedia, the free encyclopedia")]
			for i in title.split():
				yield i

	def get_bazword(self):
		return next(self._gen)

class WikipediaRandomArticle(AbstractBazwordGenerator):
	'''Scrapes random article from wikipedia and yields its words.'''
	
	def __init__(self):
		self._gen = self._generate()

	def _generate(self):
		while True:
			url = "https://en.wikipedia.org/wiki/Special:Random"
			html, _ = urlrequest.get_raw_html(url)
			soup = BeautifulSoup(html,"lxml").html
			divs = soup('div',{"id":"mw-content-text"})
			if len(divs)==0: # article is probably empty
				continue
			# this is a text of article
			article = divs[0].text
			words = article.split()
			for i in words:
				yield i

	def get_bazword(self):
		return next(self._gen)

class IncreasingNumbers(AbstractBazwordGenerator):
	def __init__(self,lower=0):
		self.state = lower

	def get_bazword(self):
		baz = str(self.state)
		self.state += 1
		return baz
		
if __name__ == "__main__":
	bg = WikipediaRandomArticleTitles()
	for i in range(1000):
		print(bg.get_bazword())
