import unittest
from ConcordanceCrawler.core.parsing import parse
from ConcordanceCrawler.core.links import *
from ConcordanceCrawler.core.bazwords import *
import requests

class TestLinks(unittest.TestCase):

	# test parsing of Bing SERP
	def test_parsing(self):
		link = "http://www.bing.com/search?q=ahoj&qs=ds&form=QBLH&scope=web"
		html = requests.get(link).text

		links = parse(html)
		
		self.assertTrue(len(links)>0)
		
		l = links[0]
		self.assertTrue('link' in l and 'snippet' in l and 'title' in l)

		self.assertTrue('http' in l['link'])

	def test_crawl_links(self):
		links = crawl_links("ahoj")
		self.assertTrue(links != [])

		for l in links:
			x = l.startswith("http")
			self.assertTrue(x)

	def test_keyword_url(self):
		url = get_keyword_url("ahoj")
		self.assertTrue(url == "http://www.bing.com/search?q=ahoj&first=1&count=59&FORM=PERE1")


	def test_bazgens(self):
		gens = [ RandomShortWords(), 
			WikipediaRandomArticle(), 
			WikipediaRandomArticleTitles(), 
			IncreasingNumbers() ]

		for g in gens:
			for i in range(10):
				baz = g.get_bazword()
				self.assertTrue(baz != "")
				self.assertTrue(" " not in baz)

if __name__=='__main__':
	unittest.main()

