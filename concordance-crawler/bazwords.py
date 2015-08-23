#!/usr/bin/env python3

"""Bazwords generators"""

import random

class RandomShortWords():
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

import requests
from bs4 import BeautifulSoup
class WikipediaRandomArticleTitles():
	'''Scrapes random article from wikipedia and yields words from its title.'''
	
	def __init__(self):
		self._gen = self._generate()

	def _generate(self):
		while True:
			x = requests.get('https://en.wikipedia.org/wiki/Special:Random').text
			pagetitle = BeautifulSoup(x,"lxml").html.head.title.string
			# there is " - Wikipedia, the free encyclopedia" in the end of every
			# page title, I'm removing it
			title = pagetitle[:-len(" - Wikipedia, the free encyclopedia")]
			for i in title.split():
				yield i

	def get_bazword(self):
		return next(self._gen)

class WikipediaRandomArticle():
	'''Scrapes random article from wikipedia and yields its words.'''
	
	def __init__(self):
		self._gen = self._generate()

	def _generate(self):
		while True:
			url = "https://en.wikipedia.org/wiki/Special:Random"
			html = requests.get(url).text
			soup = BeautifulSoup(html,"lxml").html
			# this is a text of article
			article = soup('div',{"id":"mw-content-text"})[0].text
			words = article.split()
			for i in words:
				yield i

	def get_bazword(self):
		return next(self._gen)

class IncreasingNumbers():
	def __init__(self,lower=0):
		self.state = lower

	def get_bazword(self):
		baz = str(self.state)
		self.state += 1
		return baz
		
if __name__ == "__main__":
	bg = IncreasingNumbers()
	for i in range(1000):
		print(bg.get_bazword())
