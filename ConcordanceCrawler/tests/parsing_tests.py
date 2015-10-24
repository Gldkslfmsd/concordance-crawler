import unittest
from ConcordanceCrawler.core.parsing import parse
import requests

class TestParsing(unittest.TestCase):

	# test parsing of Bing SERP
	def test_parsing(self):
		link = "http://www.bing.com/search?q=ahoj&qs=ds&form=QBLH&scope=web"
		html = requests.get(link).text

		links = parse(html)
		
		self.assertTrue(len(links)>0)
		
		l = links[0]
		self.assertTrue('link' in l and 'snippet' in l and 'title' in l)

		self.assertTrue('http' in l['link'])

if __name__=='__main__':
	unittest.main()

